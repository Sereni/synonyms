# coding=utf-8
from django.conf.urls.defaults import patterns, include, url
from dictionary.views import Index

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'synonyms.views.home', name='home'),
    # url(r'^synonyms/', include('synonyms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', Index.as_view()),
    url(r'^dictionaries/', 'dictionary.views.bibliography', name='bibliorgaphy'),
    url(r'^about/', 'dictionary.views.about', name='about'),
    url(r'^howto/', 'dictionary.views.manual', name='howto'),
)
