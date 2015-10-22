# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from loosecms.models import Row, Column, Plugin, HtmlPage, Category, PopularCategoryCloud, Configuration
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
        self.row = create_row_plugin(self.htmlpage)

    def test_default_type_row_plugin(self):
        self.assertEqual(self.row.type, self.row.default_type)

    def test_unicode_return(self):
        self.assertEqual(unicode(self.row), '%s (%s)' %(self.row.title, self.row.type))

    def test_same_order(self):
        with self.assertRaises(ValidationError):
            row = Row.objects.create(title='Second Row', slug='second-row', page=self.htmlpage, order=0)
            row.clean()

class TestConfigurationModel(TestCase):

    def setUp(self):
        self.client = Client()
        site = Site.objects.get_current()
        self.configuration = Configuration.objects.create(site=site)

    def test_unicode_return(self):
        self.assertEqual(unicode(self.configuration), self.configuration.site.name)


class TestColumnModel(TestCase):

    def setUp(self):
        self.client = Client()
        self.column = create_column_plugin(width=11)

    def test_default_type_column_plugin(self):
        self.assertEqual(self.column.type, self.column.default_type)

    def test_unicode_return(self):
        self.assertEqual(unicode(self.column), '%s (%s)' %(self.column.title, self.column.type))

    def test_same_order(self):
        with self.assertRaises(ValidationError):
            column = Column.objects.create(title='Second Column', slug='second-column', width=1, order=0)
            column.clean()

    def test_zero_width(self):
        with self.assertRaises(ValidationError):
            column = Column.objects.create(title='Second Column', slug='second-column', width=0, order=1)
            column.clean()

    def test_max_width(self):
        with self.assertRaises(ValidationError):
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


class TestHtmlPage(TestCase):

    def setUp(self):
        self.client = Client()

    def test_no_slug_checked_home(self):
        with self.assertRaises(ValidationError):
            htmlpage = HtmlPage.objects.create(title='Page', home=False)
            htmlpage.clean()

    def test_checked_home_template_error(self):
        with self.assertRaises(ValidationError):
            htmlpage = HtmlPage.objects.create(title='Page1', slug='page1', home=True, is_template=True)
            htmlpage.clean()

        with self.assertRaises(ValidationError):
            htmlpage = HtmlPage.objects.create(title='Page2', slug='page2', home=True, is_error=True)
            htmlpage.clean()

        with self.assertRaises(ValidationError):
            htmlpage = HtmlPage.objects.create(title='Page3', slug='page3', is_template=True, is_error=True)
            htmlpage.clean()

    def test_startswith_endswith(self):
        with self.assertRaises(ValidationError):
            htmlpage = HtmlPage.objects.create(title='Page1', slug='/page1')
            htmlpage.clean()

        with self.assertRaises(ValidationError):
            htmlpage = HtmlPage.objects.create(title='Page2', slug='page2/')
            htmlpage.clean()

    def test_home_unique(self):
        with self.assertRaises(ValidationError):
            htmlpage1 = HtmlPage.objects.create(title='Page1', slug='page1', home=True)
            htmlpage2 = HtmlPage.objects.create(title='Page2', slug='page2', home=True)
            htmlpage2.clean()

        try:
            htmlpage1 = HtmlPage.objects.create(title='Page3', slug='page3', home=True)
            htmlpage2 = HtmlPage.objects.create(title='Page4', slug='page4', home=True, published=False)
            htmlpage2.clean()
        except ValidationError:
            self.fail('Raised validation error unexpectedly')

    def test_error_unique(self):
        with self.assertRaises(ValidationError):
            htmlpage1 = HtmlPage.objects.create(title='Page1', slug='page1', is_error=True)
            htmlpage2 = HtmlPage.objects.create(title='Page2', slug='page2', is_error=True)
            htmlpage2.clean()

        try:
            htmlpage1 = HtmlPage.objects.create(title='Page3', slug='page3', is_error=True)
            htmlpage2 = HtmlPage.objects.create(title='Page4', slug='page4', is_error=True, published=False)
            htmlpage2.clean()
        except ValidationError:
            self.fail('Raised validation error unexpectedly')

    def test_slug_contain_namespaces(self):
        with self.assertRaises(ValidationError):
            htmlpage = HtmlPage.objects.create(title='Page', slug='/admin/page')
            htmlpage.clean()

    def test_get_absolute_url(self):
        htmlpage = HtmlPage.objects.create(title='Page1', slug='page1/page2', home=False)
        self.assertEqual(htmlpage.get_absolute_url(), '/page1/page2/')

        htmlpage = HtmlPage.objects.create(title='Page2', slug=None, home=True)
        self.assertEqual(htmlpage.get_absolute_url(), '/')


