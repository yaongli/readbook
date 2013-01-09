# -*- coding:utf-8 -*-

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User

"""
Author
    id
    name
    introduce
"""
class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'作者')
    introduce = models.TextField(blank=True, editable=True, verbose_name=u'简介')

    def __unicode__(self):
        return self.name

class Catagory(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'分类名称')
    introduce = models.TextField(blank=True, editable=True, verbose_name=u'简介')

    def __unicode__(self):
        return self.name

"""
Book
    id
    name
    author
    introduce
    createTime
    lastUpdateTime
    lastUpdateChapter
"""
class Book(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'书名')
    author = models.ForeignKey(Author, editable=True, verbose_name=u'作者')
    catagory = models.ForeignKey(Catagory, editable=True, verbose_name=u'分类')
    introduce = models.TextField(blank=True, editable=True, verbose_name=u'简介')
    cover = models.TextField(blank=True, editable=True, verbose_name=u'封面')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name=u'发布日期')
    #updateTime = models.DateTimeField(auto_now_add=True, verbose_name=u'更新日期')
    #updateChapter = models.TextField(blank=True, editable=True, verbose_name=u'最新章节')

    def __unicode__(self):
        return self.name

"""
Chapter
"""
class Chapter(models.Model):
    seq = models.IntegerField(default=0, db_index=True, verbose_name=u'排序')
    name = models.CharField(max_length=200, verbose_name=u'章节名')
    book = models.ForeignKey(Book, editable=True, verbose_name=u'书名')
    content = models.TextField(blank=True, editable=True, verbose_name=u'内容')
    updateTime = models.DateTimeField(auto_now_add=True, verbose_name=u'更新日期')
    #previous = models.IntegerField(blank=True, editable=True, verbose_name=u'上一章')
    #next = models.IntegerField(blank=True, editable=True, verbose_name=u'下一章')

    def __unicode__(self):
        return self.name

class UpdateHistory(models.Model):
    book = models.ForeignKey(Book, editable=True,verbose_name=u'书名')
    chapter = models.ForeignKey(Chapter, editable=True, verbose_name=u'更新章节')
    updateTime = models.DateTimeField(auto_now_add=True, verbose_name=u'更新日期')

"""
Reader
    id
    name
    email
    nickname
    introduce
    createTime
    lastLoginTime
"""
class Reader(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    nickname = models.CharField(max_length=50, verbose_name=u'Nick Name')
    introduce = models.TextField(blank=True, editable=True, verbose_name=u'简介')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建日期', editable=False, db_index=True)
    lastLoginTime = models.DateTimeField(auto_now_add=True, verbose_name=u'上次登录日期', editable=False, db_index=True)

    def __unicode__(self):
        return self.nickname

"""
Bookshelf
    id
    catagory
    bookid
    readerid
    authorid
    lastReadChapter
    lastUpdateChapter
"""
class BookShelf(models.Model):
    catagory = models.TextField(blank=True, editable=True, verbose_name=u'Catagory')
    book = models.ForeignKey(Book, editable=True, verbose_name=u'书名')
    author = models.ForeignKey(Author, editable=True, verbose_name=u'作者')
    lastReadChapter = models.IntegerField(blank=True, editable=True, verbose_name=u'上次阅读章节')
    lastUpdateChapter = models.IntegerField(blank=True, editable=True, verbose_name=u'最新更新章节')

    def __unicode__(self):
        return 'BookShelf'
    