# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from .plugin_pool import plugin_pool
from .models import Column, Row

from plugin_modeladmin import PluginModelAdmin


class ColumnPlugin(PluginModelAdmin):
    model = Column
    name =_('Column')
    prepopulated_fields = {'slug': ('title', )}

    def get_changeform_initial_data(self, request):
        initial = super(ColumnPlugin, self).get_changeform_initial_data(request)
        columns = self.model.objects.filter(placeholder=initial['placeholder']).order_by('order')

        order = 0
        width = 12
        for column in columns:
            width -= column.width
            if column.order == order:
                order += 1

        initial['order'] = order
        initial['width'] = width
        return initial


class RowPlugin(PluginModelAdmin):
    model = Row
    name = _('Row')
    prepopulated_fields = {'slug': ('title', )}

    def get_changeform_initial_data(self, request):
        initial = super(RowPlugin, self).get_changeform_initial_data(request)
        rows = self.model.objects.filter(placeholder=initial['placeholder'],
                                         page=initial['page']).order_by('order')

        order = 0
        for row in rows:
            if row.order == order:
                order += 1

        initial['order'] = order
        return initial

plugin_pool.register_plugin(RowPlugin)
plugin_pool.register_plugin(ColumnPlugin)