# -*- coding: utf-8 -*-

from models import *

import urllib2
import re
import os
import shutil
from Queue import Queue
import threading
import thread 

class ChapterLink():
    def __init__(self, title, href, update, num):
        title = unicode(title, 'utf-8')
        title = title.replace("*", "").replace("?", "").replace("!", "")
        self.title = title
        self.href = href
        self.update = update
        self.num = num
    
class Content():
    def __init__(self, chapter, lines):
        self.chapter = chapter
        self.lines = lines

def queryChapterLink(bookNum):
    chapterurl = r"http://www.shumilou.com/%s/" % bookNum
    webResponse = urllib2.urlopen(chapterurl)
    chapterPage = webResponse.read()
    chapterReg = r'<li class="zl"><a href="(http://www.shumilou.com/%s/\d+\.html)">(.*?)</a></li>' % bookNum
    chapterGroupList = re.findall(chapterReg, chapterPage, re.M)
    chapterList = []
    for chapterGroup in chapterGroupList:
        #print chapterGroup
        chapter = ChapterLink(chapterGroup[1], chapterGroup[0], None, None)
        chapterList.append(chapter)
    return chapterList

def queryChapterLinkList(bookurl):
    bookNum = bookurl.replace("http://www.shumilou.com/", "").replace("/", "")
    return queryChapterLink(bookNum)

def writeChapterLink(bookName, chapters):
    with open(bookName + ".txt", "w") as bookindex:
        for index,chapter in enumerate(chapters):
            line = "%s\t%s\t%s" % (index, chapter.title, chapter.href)
            line = line.encode("utf-8")
            #print line
            bookindex.write(line)
            bookindex.write("\n")
        bookindex.flush()

def queryContent(chapter):
    message = "Download %s from %s" % (chapter.title, chapter.href)
    print message
    webResponse = urllib2.urlopen(chapter.href)
    contentpage = webResponse.read()
    startposit = contentpage.find('<div class="title">')
    endposit = contentpage.find('<div class="title">', startposit + 1)
    contenttext = contentpage[startposit:endposit]
    #print "contenttext= ", contenttext
    contentReg = r'(<p>(.*?)</p>)'
    contentGroupList = re.findall(contentReg, contenttext, re.M | re.I | re.DOTALL)
    contentList = []
    for contentGroup in contentGroupList:
        #print contentGroup
        line = contentGroup[0].replace("\n", "").replace("<p>", "").replace("</p>", "")
        #line = re.sub("<span.*?</span>", "", line, re.M)
        if "" != line:
            contentList.append(line)
    
    content = Content(chapter, contentList)
    return content

def writeContent(content):
    chapter = content.chapter
    title = chapter.title
    print title
    with open(title + ".txt", "w") as writer:
        for line in content.lines:
            writer.write(line)
            writer.write("\n")

def downloadbook(bookName, bookNum):
    print "Download index ..."
    if os.path.exists(bookName):
        shutil.rmtree(bookName)
    os.makedirs(bookName)
    os.chdir(bookName)
    chapters = queryChapterLink(bookNum)
    writeChapterLink(bookName, chapters)
    print "Download content ..."
    for chapter in chapters:
        try:
            if os.path.exists(chapter.title + ".txt"):
                continue
            content = queryContent(chapter)
            writeContent(content)
        except:
            pass

def downloadchapter(book, chapterLink, chapterSequence):
    chapterName = chapterLink.title

    try:
        chapter = Chapter.objects.get(name=chapterName)
        return
    except Chapter.DoesNotExist:
        chapterSequence += 1
        content = queryContent(chapterLink)
        content = "<br/>".join(content.lines)
        chapter = Chapter(seq=chapterSequence,
            name=chapterName,
            book=book,
            content=content
            )
        chapter.save()
        try:
            updateHistory = UpdateHistory(book=book, chapter=chapter)
            updateHistory.save()
        except:
            pass

def importbook(catagoryName, bookName, authorName, bookindex):
    #
    try:
        author = Author.objects.get(name=authorName)
    except Author.DoesNotExist:
        author = Author(name=authorName)
        author.save()

    try:
        catagory = Catagory.objects.get(name=catagoryName)
    except Catagory.DoesNotExist:
        catagory = Catagory(name=catagoryName)
        catagory.save()
    #
    try:
        book = Book.objects.get(name=bookName)
    except Book.DoesNotExist:
        book = Book(name=bookName, 
            author=author, 
            catagory=catagory
            )
        book.save()
    #
    chapterLinkList = queryChapterLinkList(bookindex)
    chapterSequence = 0
    for chapterLink in chapterLinkList:
        chapterSequence += 1
        #downloadchapter(chapterLink)
        thread.start_new_thread(downloadchapter, (book, chapterLink,chapterSequence))

    return book
