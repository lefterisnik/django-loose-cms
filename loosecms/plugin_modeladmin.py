# -*- coding: utf-8 -*-
from django.template import loader
from django.contrib import admin, messages
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


class PluginModelAdmin(admin.ModelAdmin):
    template = None
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
        print "mpika"
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

