# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.conf.urls import patterns, url
from django.contrib import admin, messages
from django.utils.encoding import force_text
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _


class PluginModelAdmin(admin.ModelAdmin):

    object_successfully_added = False
    object_successfully_changed = False
    object_successfully_deleted = False

    def make_message(self, request, obj, action):
        if '_to_field' not in request.POST and '_popup' in request.POST:
            opts = self.model._meta
            msg_dict = {'name': force_text(opts.verbose_name), 'obj': force_text(obj)}
            if action == 'added':
                msg = _('The %(name)s "%(obj)s" was added successfully.') % msg_dict
            elif action == 'changed':
                msg = _('The %(name)s "%(obj)s" was changed successfully.') % msg_dict
            self.message_user(request, msg, messages.SUCCESS)

    def response_add(self, request, obj, post_url_continue=None):
        """
        Just set a flag, so we know something was changedand set the message because super sees
        _popup and dont make message. We want to make message.
        """
        self.make_message(request, obj, 'added')

        self.object_successfully_added = True

        return super(PluginModelAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        """
        Just set a flag, so we know something was changed and set the message because super sees
        _popup and dont make message. We want to make message.
        """
        self.make_message(request, obj, 'changed')

        self.object_successfully_changed = True

        return super(PluginModelAdmin, self).response_add(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        """
        Just set a flag, so we know something was changed.
        """
        self.object_successfully_deleted = True

        return super(PluginModelAdmin, self).response_delete(request, obj_display, obj_id)

    def get_urls(self):
        """
        Add custom urls to plugin manager admin.
        :return: urls
        """
        urls = super(PluginModelAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^filemanager/$', self.admin_site.admin_view(self.filemanager), name='admin_filemanager'),
        )
        return my_urls + urls

    def filemanager(self, request):
        """
        List files of specific path and give the upload input
        :return: path of selected file or uploaded file
        """
        errors = {}
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
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