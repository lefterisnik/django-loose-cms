# -*- coding: utf-8 -*-
from django.contrib import admin
from ..models import LooseCMSConfiguration


class LooseCMSConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site', 'favicon')

admin.site.register(LooseCMSConfiguration, LooseCMSConfigurationAdmin)