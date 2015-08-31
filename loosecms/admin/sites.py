# -*- coding: utf-8 -*-
from django.contrib import admin
from django.shortcuts import render
from django.conf.urls import patterns, url
from django.core.files.storage import default_storage
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _


class FileManagerAdminSite(admin.AdminSite):

    def get_urls(self):
        """
        Add custom urls to filemanager admin site.
        :return: urls
        """
        urlpatterns = patterns('',
            url(r'^filemanager/$', self.admin_view(self.filemanager), name='admin_filemanager'),
        )
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
                context.update(
                    docs=(
                        [name.split('/')[1], '/', default_storage.path(name)],
                    )
                )
        return render(request, 'admin/filemanager_form.html', context)

site = FileManagerAdminSite('filemanager')
