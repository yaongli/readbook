Introduction
------------
    This is a project that use to read book.
    The books come from internet. This project just provides a good user interface to read.

Features
--------
* Read book by chapter, whole book, several chapters,.....,etc.
* Fouverate books
* Download books
* Search by bookname or author
* Comment on chapter, paragraph, book, author
* 

Models
------

Book
    id
    name
    author
    createTime
    lastUpdateTime
    lastUpdateChapter

Chapter
    id
    bookid
    name
    
    
Author
    id
    name
    introduce

Reader
    id
    name
    email
    nickname
    introduce
    createTime
    lastLoginTime
    
Bookshelf
    id
    catagory
    bookid
    readerid
    authorid
    lastReadChapter
    lastUpdateChapter
    
    

