# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _

from ..plugin_pool import plugin_pool


class LooseCMSAdminSite(admin.AdminSite):

    def get_urls(self):
        """
        Add custom urls to loosecms admin site.
        :return: urls
        """
        urlpatterns = [
            url(r'^filemanager/$', self.admin_view(self.filemanager),
                name='admin_filemanager')
        ]

        return urlpatterns

    @never_cache
    def filemanager(self, request):
        """
        List files of specific path and give the upload input
        :return: path of selected file or uploaded file
        """
        errors = {}
        context = dict(
            # Include common variables for rendering the admin template.
            self.each_context(request),
            current_app=self.name,
            title=_('Select or Upload File'),
            is_popup=True,
            errors=errors,
        )

        if request.method == 'GET':
            if 'upload_to' in request.GET:
                upload_to = request.GET['upload_to']
                context.update(
                    upload_to=upload_to,
                )

        if request.method == 'POST':
            upload_to = request.POST['upload_to']
            context.update(
                upload_to=upload_to,
            )
            if not request.FILES:
                msg = _('This field is required.')
                errors['id_document'] = msg
                context.update(
                    errors=errors
                )
            else:
                file_ = request.FILES['document']
                filename = '%s/%s' %(upload_to, file_.name)

                name = default_storage.save(filename, file_)
                tmp = name.split('/')
                root_path = tmp[0] if len(tmp) == 2 else tmp[:-1]
                file_name = tmp[-1]
                context.update(
                    docs=(
                        [file_name, root_path, default_storage.path(name)],
                    )
                )

        return render(request, 'admin/filemanager_form.html', context)


site = LooseCMSAdminSite('loosecms')
