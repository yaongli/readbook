import os
import settings
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'book.views.home', name='home'),
    url(r'^book/(?P<bookid>\d+)/index/', 'book.views.bookindex', name="bookindex"),
    url(r'^book/(?P<bookid>\d+)/(?P<chapterid>\d+)/', 'book.views.bookchapter', name="bookchapter"),
    url(r'^author/(?P<authorid>\d+)/', 'book.views.authorpage', name="authorpage"),
    url(r'^import/shumilou/', 'book.views.importshumilou', name="importshumilou"),
    url(r'^import/shumilou/do/', 'book.views.doimportshumilou', name="doimportshumilou"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    #(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.STATIC_ROOT, 'css')}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
