# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from .helpers import *


class AdminPageViews(TestCase):

    def setUp(self):
        self.client = Client()
        get_user_model().objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='admin')

    def test_edit_page(self):
        """
        Test case of a staff user with pages in database
        Allow access, to build the page
        :return: 200
        """
        self.htmlpage = create_page(is_template=False)
        self.client.login(username='admin', password='admin')
        url = reverse('admin:admin_edit_page', args=(self.htmlpage.pk, ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_edit_template_page(self):
        """
        Test case of a staff user with pages in database to edit page
        Allow access to edit template
        :return: 200
        """
        self.htmlpage = create_page(is_template=True)
        self.client.login(username='admin', password='admin')
        url = reverse('admin:admin_edit_page', args=(self.htmlpage.pk, ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_edit_template_page_add_plugin(self):
        """
        Test case of a staff user with pages in database to add plugin at edit page
        Allow access to edit template
        :return: 200
        """
        self.htmlpage = create_page(is_template=True)
        self.client.login(username='admin', password='admin')
        row_url = reverse('admin:admin_add_placeholder', args=(self.htmlpage.pk, ))
        column_url = reverse('admin:admin_add_plugin')

        # Testing add row plugin
        response = self.client.get(row_url, {'type': 'RowPlugin'})
        self.assertEqual(response.status_code, 200)

        # Testing add column plugin
        response = self.client.get(column_url+'?type=ColumnPlugin')
        self.assertEqual(response.status_code, 200)

    # TODO: Add test at edit style of plugin
    def test_edit_template_page_edit_delete_move_plugin(self):
        """
        Test case of a staff user with template pages in database to edit plugin
        Allow access to edit plugin
        :return: 200
        """
        self.htmlpage = create_page(is_template=True)
        self.row = create_row_plugin(self.htmlpage)
        self.client.login(username='admin', password='admin')

        # Test edit row plugin
        url = reverse('admin:admin_edit_plugin', args=(self.row.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Testing delete row plugin
        url = reverse('admin:admin_delete_plugin', args=(self.row.pk, ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Testing move row plugin
        url = reverse('admin:admin_move_plugin', args=(self.row.pk, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


'''class AdminPluginViews(TestCase):

    def setUp(self):
        self.client = Client()
        get_user_model().objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='admin')'''



