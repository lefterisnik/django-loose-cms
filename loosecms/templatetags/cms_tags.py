# -*- coding: utf-8 -*-
from django import template
from django.apps import apps
from django.core import urlresolvers

from ..plugin_pool import plugin_pool

register = template.Library()

@register.simple_tag(takes_context=True)
def render_plugin(context, plugin):
    cls = plugin_pool.plugins[plugin.type]
    cls_modeladmin = cls(cls.model, None)
    # For Debugging: manager = cls_modeladmin.model.objects.get(pk=plugin.pk)
    manager = getattr(plugin, str(cls.model._meta.model_name).lower())
    return cls_modeladmin.render(context, manager)

@register.inclusion_tag('templatetags/get_available_plugin_links.html', takes_context=True)
def get_available_plugin_links(context, column):
    plugins = {}
    for plugin, cls in plugin_pool.plugins.items():
        if cls.plugin:
            app = apps.get_app_config(cls.model._meta.app_label).verbose_name
            if app in plugins:
                plugins[app][cls.name] = plugin
            else:
                plugins[app] = {}
                plugins[app][cls.name] = plugin

    context['plugins'] = plugins
    context['column'] = column
    return context

@register.simple_tag(takes_context=True)
def render_extra_admin_links(context, plugin):
    for plugin_name, cls in plugin_pool.plugins.items():
        if cls.plugin_extra_links:
            plugin_modeladmin = cls(cls.model, None)
            return plugin_modeladmin.render_link(context, plugin)

@register.inclusion_tag('templatetags/template_admin.html', takes_context=True)
def render_template_admin(context, process_column=None):
    if process_column:
        context.update({'process_column': process_column})
    else:
        context['process_column'] = 'root'
    return context

@register.inclusion_tag('templatetags/template.html', takes_context=True)
def render_template(context, parent_column=None):
    if not parent_column:
        context['process_column'] = 'root'
    else:
        context.update({'process_column': parent_column})
    return context

@register.filter
def help(value):
    return dir(value)

@register.filter
def get_verbose_name_plural(value):
    return value._meta.verbose_name_plural

@register.filter
def get_verbose_name(value):
    return value._meta.verbose_name

@register.filter
def get_class_name(value):
    return value.__class__.__name__

@register.filter
def get_dict_value(value, key):
    return value[key]

@register.filter
def get_admin_url(value, pk=None):
    if not pk:
        return urlresolvers.reverse('admin:%s' %value)
    else:
        return urlresolvers.reverse('admin:%s' %value, args=(pk,))

@register.filter
def get_tag(value):
    return value.split()[2].strip()

@register.filter
def get_plugin(value):
    plugin_pool.discover_plugins()
    plugin_modeladmin = plugin_pool.plugins[value.type](plugin_pool.plugins[value.type].model, None)
    plugin_instance = plugin_modeladmin.model.objects.get(pk=value.pk)
    return plugin_instance

@register.filter
def strip(value):
    return ' '.join(value.splitlines())