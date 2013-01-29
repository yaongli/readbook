# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escapejs
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from models import *
from forms import *
import time
from importbook import importbook as imbook

ITEMS_PER_PAGE = 20

def get_page(objs, page=ITEMS_PER_PAGE):
    paginator = Paginator(objs, ITEMS_PER_PAGE)

    try:
        ret = paginator.page(page)
    except (EmptyPage, InvalidPage):
        ret = paginator.page(paginator.num_pages)

    return ret

def get_table_rows(objs):
    cols = 4
    cols += 1
    rows = []
    colIndex = 1
    row = []
    for obj in objs:
        if colIndex % cols == 0:
            rows.append(row)
            row = []
            colIndex = 1
        else:
            row.append(obj)
            colIndex += 1
    if len(row) > 0:
        while colIndex % cols != 0:
            row.append(None)
            colIndex += 1
        rows.append(row)
    print rows
    return rows

def home(req):
    histories = get_page(UpdateHistory.objects.order_by('-updateTime'), ITEMS_PER_PAGE)
    return render_to_response('home.html', {'settings' : settings, 'histories' : histories}, context_instance=RequestContext(req))

def bookindex(req, bookid):
    bookid = int(bookid)
    print "bookid", bookid
    thebook = Book.objects.get(id=bookid)
    chapters = Chapter.objects.filter(book=bookid).order_by('seq')
    chapterRows = get_table_rows(chapters)
    
    return render_to_response('bookindex.html', {'settings' : settings, 'thebook': thebook, 'chapters' : chapters, 'chapterRows' : chapterRows}, context_instance=RequestContext(req))

def bookchapter(req, bookid, chapterid):
    bookid = int(bookid)
    chapterid = int(chapterid)
    book = Book.objects.get(id=bookid)
    chapter = Chapter.objects.get(id=chapterid)
    previousChapter = None
    nextChapter = None
    try:
        previousChapter = Chapter.objects.get(seq=(chapter.seq - 1))
    except:
        previousChapter = None
    try:
        nextChapter = Chapter.objects.get(seq=(chapter.seq + 1))
    except:
        nextChapter = None
    return render_to_response('bookchapter.html', {'settings' : settings, 'chapter' : chapter, 'book' : book, 'previousChapter' : previousChapter, 'nextChapter' : nextChapter}, context_instance=RequestContext(req))

def authorpage(req, authorid):
    author = Author.objects.get(id=authorid)
    books = Book.objects.filter(author=author)
    bookRows = get_table_rows(books)
    return render_to_response('authorpage.html', {'settings' : settings, 'author' : author, 'bookRows' : bookRows}, context_instance=RequestContext(req))

def importshumilou(req):
    if req.method == 'POST':
        form = ImportForm(req.POST)
        book = form.save(req)
        if book:
            return HttpResponseRedirect(reverse('bookindex', args=[book.id]))
    else:
        form = ImportForm({"booksite" : u"shumilou"})
    return render_to_response('import_shumilou.html', {'settings' : settings, 'form' : form}, context_instance=RequestContext(req))

def importlist(req):
    importinfolist = get_page(ImportInfo.objects.order_by('-updateTime'), ITEMS_PER_PAGE)
    return render_to_response('importinfo.html', {'settings' : settings, 'importinfolist' : importinfolist}, context_instance=RequestContext(req))

def importbook(req, importInfoId):
    importInfo = ImportInfo.objects.get(id=importInfoId)
    siteSource = importInfo.source
    if siteSource == "SHUMILOU":
        book = imbook(importInfo.catagory, importInfo.bookName, importInfo.bookAuthor, importInfo.booklink)
        if importInfo.book == None:
            importInfo.book = book
            importInfo.save()
        return HttpResponseRedirect(reverse('bookindex', args=[book.id]))
    else:
        return HttpResponseRedirect(reverse('importlist'))












