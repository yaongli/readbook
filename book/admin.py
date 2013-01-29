#!/usr/bin/env python
# coding: utf-8

from django import forms
from django.db.models import F
from book.models import *
from django.contrib import admin


############################################

class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author

class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm

admin.site.register(Author, AuthorAdmin)

############################################
admin.site.register(Catagory)
############################################

class BookAdminForm(forms.ModelForm):
    list_display = ['name', 'author', 'introduce']
    class Meta:
        model = Book

class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm

admin.site.register(Book, BookAdmin)


############################################

class ChapterAdminForm(forms.ModelForm):
    class Meta:
        model = Chapter

class ChapterAdmin(admin.ModelAdmin):
    form = ChapterAdminForm

admin.site.register(Chapter, ChapterAdmin)

############################################

class ReaderAdminForm(forms.ModelForm):
    class Meta:
        model = Reader

class ReaderAdmin(admin.ModelAdmin):
    form = ReaderAdminForm

admin.site.register(Reader, ReaderAdmin)

############################################

class BookShelfAdminForm(forms.ModelForm):
    class Meta:
        model = BookShelf

class BookShelfAdmin(admin.ModelAdmin):
    form = BookShelfAdminForm

admin.site.register(BookShelf, BookShelfAdmin)

admin.site.register(UpdateHistory)


#################################
admin.site.register(ImportInfo)

