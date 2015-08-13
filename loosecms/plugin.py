# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from .plugin_pool import plugin_pool
from .models import ColumnManager, RowManager
from .forms import ColumnManagerForm, RowManagerForm

from plugin_modeladmin import PluginModelAdmin


class ColumnPlugin(PluginModelAdmin):
    model = ColumnManager
    name =_('Column')
    form = ColumnManagerForm
    plugin = False
    prepopulated_fields = {'slug': ('title', )}
    extra_initial_help = None
    fields = ('type', 'placeholder', 'title', 'slug', 'width', 'order', 'published')

    def get_changeform_initial_data(self, request):
        initial = {}
        if self.extra_initial_help:
            initial['type'] = self.extra_initial_help['type']
            initial['placeholder'] = self.extra_initial_help['placeholder']

            columns = ColumnManager.objects.filter(placeholder=self.extra_initial_help['placeholder']).order_by('order')

            order = 0
            width = 12
            for column in columns:
                width -= column.width
                if column.order == order:
                    order += 1

            initial['order'] = order
            initial['width'] = width
            return initial
        else:
            return {'type': 'ColumnPlugin'}


class RowPlugin(PluginModelAdmin):
    model = RowManager
    name = _('Row')
    form = RowManagerForm
    plugin = False
    prepopulated_fields = {'slug': ('title', )}
    extra_initial_help = None
    fields = ('type', 'placeholder', 'title', 'slug', 'page', 'order', 'published')

    def get_changeform_initial_data(self, request):
        initial = {}
        if self.extra_initial_help:
            initial['type'] = self.extra_initial_help['type']
            initial['placeholder'] = self.extra_initial_help['placeholder']
            initial['page'] = self.extra_initial_help['page']

            rows = self.model.objects.filter(placeholder=self.extra_initial_help['placeholder'],
                                             page=self.extra_initial_help['page']).order_by('order')
            order = 0
            for row in rows:
                if row.order == order:
                    order += 1

            initial['order'] = order
            return initial
        else:
            return {'type': 'RowPlugin'}

plugin_pool.register_plugin(RowPlugin)
plugin_pool.register_plugin(ColumnPlugin)