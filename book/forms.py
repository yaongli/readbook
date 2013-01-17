# -*- coding: utf-8 -*-
import re
import random
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import importbook

class ImportForm(forms.Form):
    booksite = forms.CharField(label=u'Book Site', required=True, max_length=64, widget=forms.TextInput(attrs={'tabindex': '1', "class" : "span4"}))
    bookname = forms.CharField(label=u'Book Name', required=True, max_length=64, widget=forms.TextInput(attrs={'tabindex': '2', "class" : "span4"}))
    authorname = forms.CharField(label=u'Author Name', required=True, max_length=30, widget=forms.TextInput(attrs={'tabindex': '3', "class" : "span4"}))
    bookurl = forms.CharField(label=u'Index URL', required=True, max_length=128, widget=forms.TextInput(attrs={'tabindex': '4', "class" : "span4"}))
    catagory = forms.CharField(label=u'Catagory', required=True, max_length=128, widget=forms.TextInput(attrs={'tabindex': '4', "class" : "span4"}))

    def clean_booksite(self):
        booksite = self.cleaned_data['booksite'].strip()
        return booksite
    
    def clean_bookname(self):
        bookname = self.cleaned_data['bookname'].strip()
        return bookname

    def clean_authorname(self):
        authorname = self.cleaned_data['authorname'].strip()
        return authorname
    
    def clean_bookurl(self):
        bookurl = self.cleaned_data['bookurl'].strip()
        return bookurl

    def clean_catagory(self):
        catagory = self.cleaned_data['catagory'].strip()
        return catagory

    def save(self, request):
        if not self.is_valid():
            return False
        booksite = self.cleaned_data['booksite']
        bookname = self.cleaned_data['bookname']
        authorname = self.cleaned_data['authorname']
        bookurl = self.cleaned_data['bookurl']
        catagory = self.cleaned_data['catagory']
        book = importbook.importbook(catagory, bookname, authorname, bookurl)
        
        return book
