# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.contrib import admin, messages


class PluginModelAdmin(admin.ModelAdmin):

    object_successfully_added = False
    object_successfully_changed = False
    object_successfully_deleted = False

    def make_message(self, request, obj, action):
        if '_to_field' not in request.POST and '_popup' in request.POST:
            opts = self.model._meta
            msg_dict = {'name': force_text(opts.verbose_name),
                        'obj': force_text(obj),
                        'action': force_text(action)}
            msg = _('The %(name)s "%(obj)s" was (action) successfully.') % msg_dict
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