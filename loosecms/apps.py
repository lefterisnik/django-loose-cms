# -*- coding: utf-8 -*-
from django.apps import AppConfig, apps
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.db import ProgrammingError, OperationalError


from .utils.setup import setup
from .plugin_pool import plugin_pool


class LooseCMSConfig(AppConfig):
    name = 'loosecms'
    verbose_name = _('Loose CMS')

    def ready(self):
        setup()

        # Import all plugins
        plugin_pool.discover_plugins()

        # Import all plugin urls
        plugin_pool.discover_plugin_urls()

        # Get values for settings file
        SiteApp = apps.get_app_config('sites')
        Site = SiteApp.get_model('Site')
        try:
            current_site = Site.objects.get_current()
        except (ProgrammingError, OperationalError) as e:
            return
        except Site.DoesNotExist:
            raise ObjectDoesNotExist("In settings.py you set wrong SITE_ID. Please set the SITE_ID to match "
                                     "with these from database.")

        # Here we can add settings to settings.py and change it dynamically with model signals



