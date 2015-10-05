from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('loosecms.urls')),
]

handler404 = 'loosecms.views.error404'



