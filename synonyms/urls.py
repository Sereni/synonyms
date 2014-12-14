# coding=utf-8
from django.conf.urls.defaults import patterns, include, url
from dictionary.views import Index, Bibliography, About, Manual

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
    url(r'^dictionaries/', Bibliography.as_view()),
    url(r'^about/', About.as_view()),
    url(r'^howto/', Manual.as_view()),
)
