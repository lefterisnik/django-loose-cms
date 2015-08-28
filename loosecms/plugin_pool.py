# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.importlib import import_module


class PluginPool(object):
    def __init__(self):
        """
        Initialize plugins dict
        :return: None
        """
        self.plugins = {}

    def clear(self):
        """
        Clear plugin dict
        :return: None
        """
        self.plugins = {}

    def discover_plugins(self):
        """
        Discover plugin by installed apps and importing plugin.py from every plugin
        :return: None
        """
        modname = 'plugin'
        for app in settings.INSTALLED_APPS:
            module_name = '%s.%s' % (app, modname)
            try:
                module = import_module(module_name)
            except Exception, e:
                continue

    def register_plugin(self, plugin):
        """
        Registers the given plugin(s).

        If a plugin is already registered, this will raise PluginAlreadyRegistered.
        """
        plugin_name = plugin.__name__
        plugin.value = plugin_name
        self.plugins[plugin_name] = plugin

    def unregister_plugin(self, plugin):
        """
        Unregisters the given plugin(s).

        If a plugin isn't already registered, this will raise PluginNotRegistered.
        """
        plugin_name = plugin.__name__
        del self.plugins[plugin_name]

plugin_pool = PluginPool()