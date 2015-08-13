# -*- coding: utf-8 -*-
import operator
from django.db.models import Q
from .models import Plugin, ColumnManager, RowManager


def get_sort_list(list, item):
    return sorted(list, key=operator.attrgetter(item))


def update_context(context, page=None):
    if page:
        # Get all row (otherwise placeholder) from the current page and template
        query_rows = RowManager.objects.select_related('placeholder').filter(Q(page=page) | Q(page=page.template),
                                                                             published=True)
        # Get all columns tha have as parent placeholder the rows that appear to this page
        query_columns = ColumnManager.objects.select_related('placeholder').filter(Q(placeholder__rowmanager__page=page) | Q(placeholder__rowmanager__page=page.template),
                                                                                   published=True)
        # Get all plugins except RowPlugin and ColumnPlugin
        query_plugins = Plugin.objects.select_related('placeholder').filter(~Q(type='RowPlugin'),
                                                                            ~Q(type='ColumnPlugin'),
                                                                            published=True)

        rows = list(query_rows)
        columns = list(query_columns)
        plugins = list(query_plugins)

        processing_rows = {}
        for column in columns:
            tmp_rows = []
            for row in rows:
                if row.placeholder:
                    if row.placeholder.pk == column.pk:
                        tmp_rows.append(row)
            tmp_rows = get_sort_list(tmp_rows, 'order')
            if len(tmp_rows) > 0:
                processing_rows[column] = tmp_rows

        processing_columns = {}
        for row in rows:
            tmp_columns = [column for column in columns if column.placeholder.pk == row.pk]
            tmp_columns = get_sort_list(tmp_columns, 'order')
            if tmp_columns > 0:
                processing_columns[row] = tmp_columns

        processing_plugins = {}
        for column in columns:
            tmp_plugin = [plugin for plugin in plugins if plugin.placeholder.pk == column.pk]
            if len(tmp_plugin) > 0:
                processing_plugins[column] = tmp_plugin[0]

        processing_rows['root'] = [row for row in rows if not row.placeholder]
        processing_rows['root'] = get_sort_list(processing_rows['root'], 'order')

        context['processing_rows'] = processing_rows
        context['processing_columns'] = processing_columns
        context['processing_plugins'] = processing_plugins
        return context
    else:
        context['processing_rows'] = dict(root=[])
        context['processing_columns'] = dict()
        context['processing_plugins'] = dict()
        return context



