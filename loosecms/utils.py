# -*- coding: utf-8 -*-
import tinycss
import operator
import collections
from django.db.models import Q
from HTMLParser import HTMLParser
from .models import Plugin, ColumnManager, RowManager, Style, StyleClass, StyleClassInherit


## Functions for collecting the grid of a page

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


## Function for edit style form

def populate_cssclasses_attrs(csss, plugin_style_inst):
    # For each css, parse it with tinycss and exam if id or class exist in them
    # and then take the attrs or declarations according to tinycss
    for css in csss:
        css_parser = tinycss.make_parser('page3')
        stylesheet = css_parser.parse_stylesheet_file(css)

        for html_tag in plugin_style_inst.html_tags:
            for rule in stylesheet.rules:
                if not rule.at_keyword:
                    for css_class in html_tag.classes:
                        if rule.selector.as_css().endswith(".%s" % css_class.name):
                            css_class.attrs[rule.selector.as_css()] = list(rule.declarations)
                    if rule.selector.as_css().endswith("#%s" % html_tag.id):
                        for declaration in rule.declarations:
                            html_tag.style += '%s: %s' % (declaration.name, declaration.value.as_css())


def get_initial_values(plugin_style_inst):
    return [get_dict(html_tag) for html_tag in plugin_style_inst.html_tags]


def get_dict(html_tag):
    return {
        'original_html': html_tag.original,
        'html_tag': html_tag.name,
        'html_id': html_tag.id,
        'styleclasses': get_styleclasses(html_tag),
        'css': html_tag.style,
        'position': html_tag.position
    }


def get_styleclasses(html_tag):
    defaults = []
    for class_ in html_tag.classes:
        try:
            styleclass = StyleClass.objects.get(title=class_.name, override=False)
            # TODO: if override is False then user don't change it (add extra attrs )
            # so it is safe to update class attrs
        except StyleClass.DoesNotExist:
            styleclass = StyleClass(title=class_.name, from_source=True)
            styleclass.save()

        for attr in class_.attrs:

            css = '%s\n' % ('\n'.join(x.name + ": " + x.value.as_css() + ";" for x in class_.attrs[attr]))
            try:
                styleclassinherit = StyleClassInherit.objects.get(title=attr)
            except StyleClassInherit.DoesNotExist:
                styleclassinherit = StyleClassInherit(title=attr, css=css,
                                                      styleclass=styleclass)
                styleclassinherit.save()

        defaults.append(styleclass)

    return [x.pk for x in defaults]


## Classes for the parsing html plugin's template

class PluginStyle(object):
    def __init__(self, html_tags=None, css_classes=None):
        if html_tags is None:
            self.html_tags = []
        else:
            self.html_tags = html_tags

    def exam_if_tag_exist(self, htmltag_inst):
        if len(self.html_tags) != 0:
            for html_tag in self.html_tags:
                if html_tag.name == htmltag_inst.name and \
                                html_tag.classes == htmltag_inst.classes and \
                                html_tag.id == htmltag_inst.id:
                    html_tag.update_position(htmltag_inst.position)
                    return True
        return False

    def exam_if_class_exist(self, class_name):
        for html_tag in self.html_tags:
            for css_class in html_tag.classes:
                if class_name == css_class.name:
                    return css_class
        return False


class CssClass(object):
    def __init__(self, name, attrs=None):
        self.name = name
        if attrs is None:
            self.attrs = dict()
        else:
            self.attrs = attrs


class HtmlTag(object):
    def __init__(self, name, original=None, position=None, id=None, classes=None, style=""):
        self.name, self.id, self.style, self.original = name, id, style, original
        if classes is None:
            self.classes = []
        else:
            self.classes = classes

        if position is None:
            self.position = ()
        else:
            self.position = position

    def add_class_inst(self, class_inst):
        self.classes.append(class_inst)

    def set_id(self, id_name):
        self.id = id_name

    def set_style(self, style):
        self.style = style

    def update_position(self, position):
        if isinstance(self.position, tuple):
            self.position = [self.position]
        self.position.append(position)



class MyHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.plugin_style = PluginStyle()

    def handle_starttag(self, tag, attrs):
        html_tag = HtmlTag(name=tag, position=self.getpos())
        html_tag.original = self.get_starttag_text()

        for attr in attrs:
            if attr[0] == 'class':
                for class_ in attr[1].split():
                    exist = self.plugin_style.exam_if_class_exist(class_)
                    if not exist :
                        css_class = CssClass(name=class_)
                        html_tag.add_class_inst(css_class)
                    else:
                        html_tag.add_class_inst(exist)
            if attr[0] == 'id':
                html_tag.set_id(attr[1])
            if attr[0] == 'style':
                html_tag.set_style(attr[1])


        if not self.plugin_style.exam_if_tag_exist(html_tag):
            self.plugin_style.html_tags.append(html_tag)

