# -*- coding: utf-8 -*-
from django.conf import settings
from django.apps import AppConfig
from django.contrib.sites.apps import SitesConfig
from django.utils.translation import ugettext_lazy as _


from loosecms.utils.setup import setup
from loosecms.plugin_pool import plugin_pool


class LooseCMSConfig(AppConfig):
    name = 'loosecms'
    verbose_name = _('Loose CMS')

    def ready(self):
        setup()

        # Import all plugins
        plugin_pool.discover_plugins()


class LooseCMSSiteConfig(SitesConfig):

    def ready(self):
        super(LooseCMSSiteConfig, self).ready()

        # Load configs from database
        LooseCMSConfiguration = self.get_model('LooseCMSConfiguration')
        Site = self.get_model('Site')
        current_site = Site.objects.get_current()
        print current_site