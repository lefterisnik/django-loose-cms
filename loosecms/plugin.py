# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .plugin_pool import plugin_pool
from .models import Column, Row, Category, PopularCategoryCloud, LoosecmsTag
from .plugin_modeladmin import PluginModelAdmin


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


class CategoryPlugin(PluginModelAdmin):
    model = Category
    template = 'plugin/category.html'
    name = _('Category search results')
    plugin = True
    prepopulated_fields = {'slug': ('title', )}

    def update_context(self, context, manager):
        request = context['request']
        if request.method == 'GET':
            if 'category' in request.GET:
                category = request.GET['category']
                try:
                    loosecmstag = LoosecmsTag.objects.get(name=category)
                    loosecmstagged = loosecmstag.loosecms_loosecmstagged_items.all()

                    if manager.number:
                        paginator = Paginator(loosecmstagged, manager.number)
                        pageset = context['request'].GET.get('pageset')
                        try:
                            loosecmstagged = paginator.page(pageset)
                        except PageNotAnInteger:
                            loosecmstagged = paginator.page(1)
                        except EmptyPage:
                            loosecmstagged = paginator.page(paginator.num_pages)

                    context['loosecmstagged'] = loosecmstagged
                    context['category'] = category
                except LoosecmsTag.DoesNotExist:
                    context['category'] = category
                return context
            else:
                return context


class PopularCategoryCloudPlugin(PluginModelAdmin):
    model = PopularCategoryCloud
    template = 'plugin/popular_categorycloud.html'
    name = _('Category cloud')
    plugin = True
    prepopulated_fields = {'slug': ('title', )}

    def update_context(self, context, manager):
        categories = LoosecmsTag.objects.all()
        context['categories'] = categories
        context['categorycloud'] = manager
        return context


plugin_pool.register_plugin(CategoryPlugin)
plugin_pool.register_plugin(PopularCategoryCloudPlugin)
plugin_pool.register_plugin(RowPlugin)
plugin_pool.register_plugin(ColumnPlugin)