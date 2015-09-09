# -*- coding: utf-8 -*-
from django.template import loader
from django.contrib import admin, messages
from django.utils.encoding import force_text
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from .forms import PluginForm


class PluginModelAdmin(admin.ModelAdmin):
    change_form_template = 'admin/plugin_change_form.html'
    delete_confirmation_template = 'admin/plugin_delete_form.html'
    form = PluginForm

    extra_initial_help = None
    template = None
    template_cke = None
    plugin = False
    plugin_cke = False
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
        Just set a flag, so we know something was changed and set the message because super sees
        _popup and dont make message. We want to make message.
        """
        self.make_message(request, obj, 'added')

        self.object_successfully_added = True
        if self.plugin_cke:
            context = dict(
                obj=obj,
            )
            element = self.render_to_string_cke(context, obj)
            return HttpResponse("<script>window.parent.LooseCMS.CKEditor['element'] = '%s';</script>" % element)

        return super(PluginModelAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        """
        Just set a flag, so we know something was changed and set the message because super sees
        _popup and dont make message. We want to make message.
        """
        self.make_message(request, obj, 'changed')

        self.object_successfully_changed = True

        if self.plugin_cke:
            context = dict(
                obj=obj,
            )
            element = self.render_to_string_cke(context, obj)
            return HttpResponse("<script>window.parent.LooseCMS.CKEditor['element'] = '%s';</script>" % element)

        if '_to_field' not in request.POST and '_popup' in request.POST:
            return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')

        return super(PluginModelAdmin, self).response_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        """
        Just set a flag, so we know something was changed.
        """
        self.object_successfully_deleted = True

        return super(PluginModelAdmin, self).response_delete(request, obj_display, obj_id)

    def get_fields(self, request, obj=None):
        """
        Move published field to the end of the list
        :param request:
        :param obj:
        :return:
        """
        fields = super(PluginModelAdmin, self).get_fields(request, obj)
        fields.pop(fields.index('published'))
        fields.append('published')

        return fields

    def get_changeform_initial_data(self, request):
        """
        Set extra initial data. Maybe some of them may be unnecessary.
        :param request:
        :return: initial data
        """
        initial = super(PluginModelAdmin, self).get_changeform_initial_data(request)
        if self.extra_initial_help:
            initial.update(
                placeholder = self.extra_initial_help['placeholder'],
                page = self.extra_initial_help['page'],
            )

        initial.update(
            type=self.model.default_type
        )
        return initial

    def update_context(self, context, manager):
        """
        You should override this function to add values to context
        :param context:
        :param manager:
        :return: Context
        """
        return context

    def render(self, context, manager):
        """
        Render to html the plugin
        :param context:
        :param manager:
        :return: HTML
        """
        context = self.update_context(context, manager)
        template = loader.get_template(self.template)
        return template.render(context)

    def render_to_string(self, context, manager):
        """
        Render to string the plugin. This is used by stylesheet action
        :param context:
        :param manager:
        :return: String html of the plugin
        """
        context = self.update_context(context, manager)
        return loader.render_to_string(self.template, context)

    def render_to_string_cke(self, context, obj):
        """
        Render to string the plugin for the element of ckeditor
        :param context:
        :param obj:
        :return:
        """
        context = self.update_context(context, obj)
        return loader.render_to_string(self.template_cke, context)


class PluginModelInlineAdmin(admin.StackedInline):
    form = PluginForm
    show_change_link = True
    extra = 1

    def get_fields(self, request, obj=None):
        """
        Move published field to the end of the list
        :param request:
        :param obj:
        :return:
        """
        fields = super(PluginModelInlineAdmin, self).get_fields(request, obj)
        fields.pop(fields.index('published'))
        fields.append('published')

        return fields