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
        self.extra_urlpatterns = []
        self.embed_urlpatterns = []

    def clear(self):
        """
        Clear plugin dict
        :return: None
        """
        self.plugins = {}

    def discover_plugin_urls(self):
        """
        Discover plugin extra urls and added to extra_urlpatterns or embed_urlpatterns
        :return: None
        """
        modname = 'urls'
        for app in settings.INSTALLED_APPS:
            try:
                if 'loosecms_' in app:
                    module_name = '%s.%s' %(app, modname)
                    module = import_module(module_name)
                    try:
                        self.extra_urlpatterns += module.urlpatterns
                    except Exception, e:
                        # urlpatterns is not defined
                        pass

                    try:
                        self.embed_urlpatterns += module.embed_urlpatterns
                    except Exception,e:
                        # embed_urlpatterns is not defined
                        pass
            except Exception, e:
                continue

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