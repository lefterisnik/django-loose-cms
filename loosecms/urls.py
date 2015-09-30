# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static

from .views import *
from .utils.urls import *
from .admin.sites import site

handler404 = error404

# Get the extra urls from plugins. Extra urlpatterns represent the extra root urls and embed urlpatterns represent urls
# that extend page url.
extra_urlpatterns, embed_urlpatterns = get_app_urls()

# Initialization of the urlpatterns. First append all extra urlconfs of plugins, then add only the view for page index
# and finally append the home page pattern
urlpatterns = [
    url(r'^cms/', include(extra_urlpatterns)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^(?P<page_slug>[0-9A-Za-z-_.//]+)/', include(embed_urlpatterns)),
    url(r'^(?P<page_slug>[0-9A-Za-z-_.//]+)/$', detail, name='pages-info'),
    url(r'^$', detail, {'page_slug': ''}, name='pages-home'),
]

if settings.DEBUG:
    media_url = getattr(settings, 'MEDIA_URL', None)
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if media_url and media_root:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)