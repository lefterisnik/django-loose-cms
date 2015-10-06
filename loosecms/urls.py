# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from .views import *
from .utils.urls import *
from .admin.sites import site

from .plugin_pool import plugin_pool

# Import all plugin urls
plugin_pool.discover_plugin_urls()
# Get the extra urls from plugins. Extra urlpatterns represent the extra root urls and embed urlpatterns represent urls
# that extend page url.
extra_urlpatterns, embed_urlpatterns = get_app_urls()

# Initialization of the urlpatterns. First append all extra urlconfs of plugins, then add only the view for page index
# and finally append the home page pattern
urlpatterns = [
    url(r'^cms/', include(extra_urlpatterns)),
    url(r'^admin/', include(site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^(?P<page_slug>[0-9A-Za-z-_.//]+)/', include(embed_urlpatterns)),
    url(r'^(?P<page_slug>[0-9A-Za-z-_.//]+)/$', detail, name='pages-info'),
    url(r'^$', detail, {'page_slug': ''}, name='pages-home'),
]