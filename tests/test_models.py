# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.core.exceptions import ValidationError
from loosecms.models import Row, Column, Plugin, HtmlPage, Category, PopularCategoryCloud
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
        self.row = Row.objects.create(title='Row', slug='row', page=self.htmlpage, order=0)


    def test_default_type_row_plugin(self):
        self.assertEqual(self.row.type, self.row.default_type)

    def test_unicode_return(self):
        self.assertEqual(unicode(self.row), '%s (%s)' %(self.row.title, self.row.type))

    def test_same_order(self):
        msg = 'In this place a plugin is already exist. Please change the order.'
        with self.assertRaisesMessage(ValidationError, msg):
            row = Row.objects.create(title='Second Row', slug='second-row', page=self.htmlpage, order=0)
            row.clean()


class TestColumnModel(TestCase):

    def setUp(self):
        self.client = Client()
        self.column = Column.objects.create(title='Column', slug='column', width=11, order=0)

    def test_default_type_column_plugin(self):
        self.assertEqual(self.column.type, self.column.default_type)

    def test_unicode_return(self):
        self.assertEqual(unicode(self.column), '%s (%s)' %(self.column.title, self.column.type))

    def test_same_order(self):
        msg = 'In this place a plugin is already exist. Please change the order.'
        with self.assertRaisesMessage(ValidationError, msg):
            column = Column.objects.create(title='Second Column', slug='second-column', width=1, order=0)
            column.clean()

    def test_zero_width(self):
        msg = 'Width value must be larger than 0.'
        with self.assertRaisesMessage(ValidationError, msg):
            column = Column.objects.create(title='Second Column', slug='second-column', width=0, order=1)
            column.clean()

    def test_max_width(self):
        msg = 'Width value is too big. The valid maximum value is 1.'
        with self.assertRaisesMessage(ValidationError, msg):
            column = Column.objects.create(title='Second Column', slug='second-column', width=2, order=1)
            column.clean()


class TestCategoryModel(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(title='Category', slug='category')

    def test_unicode_return(self):
        self.assertEqual(unicode(self.category), '%s (%s)' %(self.category.title, self.category.type))


class TestPopularCategoryModel(TestCase):

    def setUp(self):
        self.client = Client()
        self.htmlpage = create_page()
        self.popularcategorycloud = PopularCategoryCloud.objects.create(title='Category Cloud',
                                                                        slug='category-cloud',
                                                                        page=self.htmlpage)

    def test_unicode_return(self):
        self.assertEqual(unicode(self.popularcategorycloud),
                         '%s (%s)' %(self.popularcategorycloud.title, self.popularcategorycloud.type))

