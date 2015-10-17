# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from loosecms.models import Row, Column, Plugin, HtmlPage
from .helpers import *


class TestPluginModel(TestCase):

    def setUp(self):
        self.client = Client()

    def test_default_type_plugin(self):
        plugin = Plugin.objects.create()
        plugin.default_type = 'PluginExample'
        plugin.save()
        self.assertEqual(plugin.type, 'PluginExample')


class TestRowModel(TestCase):

    def setUp(self):
        self.client = Client()
        self.htmlpage = create_page()

    def test_default_type_row_plugin(self):
        row = Row.objects.create(title='Row', slug='row', page=self.htmlpage)
        self.assertEqual(row.type, row.default_type)


class TestColumnModel(TestCase):

    def setUp(self):
        self.client = Client()

    def test_default_type_column_plugin(self):
        column = Column.objects.create(title='Column', slug='column', width=12)
        self.assertEqual(column.type, column.default_type)

