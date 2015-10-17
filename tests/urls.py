# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import include, url
from loosecms.conf.urls.i18n import simple_i18n_patterns

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += simple_i18n_patterns(
    url(r'^', include('loosecms.urls')),
)

handler404 = 'loosecms.views.error404'
