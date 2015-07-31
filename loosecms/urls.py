# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from .views import *

extra_urlpatterns = []

app_urlpatterns = []

# Find all urlconfs of all plugins and add thus to extra_patterns
modname = 'urls'
for app in settings.INSTALLED_APPS:
    try:
        if 'tscms_' in app:
            module_name = '%s.%s' %(app, modname)
            module = import_module(module_name)
            extra_urlpatterns += module.urlpatterns
            app_urlpatterns += module.app_urlpatterns
    except Exception, e:
        continue

urlpatterns = app_urlpatterns

# Initialization of the urlpatterns. First append all extra urlconfs of plugins, then add only the view for page index
# and finally append the home page pattern
urlpatterns += [
    url(r'^(?P<page_slug>[0-9A-Za-z-_.]+)/', include(extra_urlpatterns)),
    url(r'^(?P<page_slug>[0-9A-Za-z-_.]+)/(?P<category_slug>[0-9A-Za-z-_.]+)/$', detail, name='category-info'),
    url(r'^(?P<page_slug>[0-9A-Za-z-_.]+)/(?P<category_slug>[0-9A-Za-z-_.]+)/(?P<slug>[0-9A-Za-z-_.]+)/$', detail, name='info'),
    url(r'^(?P<page_slug>[0-9A-Za-z-_.]+)/$', detail, name='pages-info'),
    url(r'^$', detail, {'page_slug': '', 'category_slug': '', 'slug': ''}, name='pages-home'),
]