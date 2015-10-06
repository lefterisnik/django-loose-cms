# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import Style, StyleClass, StyleClassInherit, Configuration, LoosecmsTag

from taggit.models import Tag


class StyleAdmin(admin.ModelAdmin):
    filter_horizontal = ('styleclasses',)
    #form = StyleForm

    #def __init__(self, model, admin_site):
    #    self.form.admin_site = admin_site
    #    super(StyleAdmin, self).__init__(model, admin_site)


class StyleClassInheritInline(admin.StackedInline):
    model = StyleClassInherit
    extra = 1


class StyleClassAdmin(admin.ModelAdmin):
    inlines = [
        StyleClassInheritInline
    ]


class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_site', 'favicon')

    def get_site(self, obj):
        return obj.site.name

    get_site.short_description = _('Site')
    get_site.admin_order_field = 'site__name'


admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Style, StyleAdmin)
admin.site.register(StyleClassInherit)
admin.site.register(LoosecmsTag)
admin.site.unregister(Tag)
admin.site.register(StyleClass, StyleClassAdmin)