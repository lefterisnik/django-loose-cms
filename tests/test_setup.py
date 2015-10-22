# -*- coding: utf-8 -*-
from django.apps import apps
from django.test import Client, TestCase
from django.core.exceptions import ImproperlyConfigured


class TestSetup(TestCase):

    def setUp(self):
        self.client = Client()
        self.appconfig = apps.get_app_config('loosecms')

    def test_installed_apps(self):
        with self.assertRaises(ImproperlyConfigured):
            with self.modify_settings(INSTALLED_APPS={
                'remove': [
                    'django_admin_bootstrapped',
                ]
            }):
                self.appconfig.ready()

            with self.modify_settings(INSTALLED_APPS={
                'remove': [
                    'ckeditor',
                ]
            }):
                self.appconfig.ready()

            with self.modify_settings(INSTALLED_APPS={
                'remove': [
                    'django.contrib.humanize',
                ]
            }):
                self.appconfig.ready()


