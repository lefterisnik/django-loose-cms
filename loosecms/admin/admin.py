# -*- coding: utf-8 -*-
from django.contrib import admin
from ..models import Style, StyleClass, StyleClassInherit


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

admin.site.register(Style, StyleAdmin)
admin.site.register(StyleClassInherit)
admin.site.register(StyleClass, StyleClassAdmin)