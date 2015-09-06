# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .utils.setup import setup
from .plugin_pool import plugin_pool


class LooseCMSConfig(AppConfig):
    name = 'loosecms'
    verbose_name = _('Loose CMS')

    def ready(self):
        setup()

        # Import all plugins
        plugin_pool.discover_plugins()