# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import Configuration, LoosecmsTag

from taggit.models import Tag


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_site', 'favicon')

    def get_site(self, obj):
        return obj.site.name

    get_site.short_description = _('Site')
    get_site.admin_order_field = 'site__name'


admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(LoosecmsTag)
admin.site.unregister(Tag)
