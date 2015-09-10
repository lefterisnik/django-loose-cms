# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.utils.importlib import import_module

from .views import *
from .admin.sites import site

handler404 = error404
extra_urlpatterns = []
app_urlpatterns = []

# Find all urlconfs of all plugins and add thus to extra_patterns
modname = 'urls'
for app in settings.INSTALLED_APPS:
    try:
        if 'loosecms_' in app:
            module_name = '%s.%s' %(app, modname)
            module = import_module(module_name)
            extra_urlpatterns += module.urlpatterns
            app_urlpatterns += module.app_urlpatterns
    except Exception, e:
        continue

urlpatterns = app_urlpatterns

if settings.DEBUG:
    media_url = getattr(settings, 'MEDIA_URL', None)
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if media_url and media_root:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Initialization of the urlpatterns. First append all extra urlconfs of plugins, then add only the view for page index
# and finally append the home page pattern
urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^(?P<page_slug>[0-9A-Za-z-_.]+)/', include(extra_urlpatterns)),
    url(r'^(?P<page_slug>[0-9A-Za-z-_.]+)/(?P<category_slug>[0-9A-Za-z-_.]+)/$', detail, name='category-info'),
    url(r'^(?P<page_slug>[0-9A-Za-z-_.]+)/(?P<category_slug>[0-9A-Za-z-_.]+)/(?P<slug>[0-9A-Za-z-_.]+)/$', detail, name='info'),
    url(r'^(?P<page_slug>[0-9A-Za-z-_.]+)/$', detail, name='pages-info'),
    url(r'^$', detail, {'page_slug': '', 'category_slug': '', 'slug': ''}, name='pages-home'),
]