# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse, resolve
from .helpers import *


class AdminPageViews(TestCase):

    def setUp(self):
        self.client = Client()
        get_user_model().objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='admin')
        self.client.login(username='admin', password='admin')

    def test_edit_page(self):
        """
        Test case of a staff user with pages in database
        Allow access, to build the page
        :return: 200
        """
        self.htmlpage = create_page(is_template=False)
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
        row_url = reverse('admin:admin_add_placeholder', args=(self.htmlpage.pk, ))
        column_url = reverse('admin:admin_add_plugin')

        # Testing add row plugin
        response = self.client.get(row_url, {'type': 'RowPlugin'})
        self.assertEqual(response.status_code, 200)

        # Testing add column plugin
        response = self.client.get(column_url+'?type=ColumnPlugin')
        self.assertEqual(response.status_code, 200)

    def test_edit_template_page_edit_delete_move_plugin(self):
        """
        Test case of a staff user with template pages in database to edit plugin
        Allow access to edit plugin
        :return: 200
        """
        self.htmlpage = create_page(is_template=True)
        self.row = create_row_plugin(self.htmlpage)

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

    def test_htmlpage_add_view_popup_var_true(self):
        htmlpage = create_page()

        edit_page_url = reverse('admin:admin_edit_page', args=(htmlpage.pk, ))
        detail_page_url = '/page1/'

        add_url = reverse('admin:%s_%s_add' %('loosecms', 'htmlpage'))

        response = self.client.get(add_url, HTTP_REFERER=edit_page_url)
        self.assertEqual(response.context['is_popup'], True)

        response = self.client.get(add_url, HTTP_REFERER=detail_page_url)
        self.assertEqual(response.context['is_popup'], True)

    def test_htmlpage_add_view_popup_var_false(self):
        htmlpage = create_page()

        add_url = reverse('admin:%s_%s_add' %('loosecms', 'htmlpage'))
        changelist_url = reverse('admin:%s_%s_changelist' %('loosecms', 'htmlpage'))

        response = self.client.get(add_url)
        self.assertEqual(response.context['is_popup'], False)

        response = self.client.get(add_url, HTTP_REFERER=changelist_url)
        self.assertEqual(response.context['is_popup'], False)

    def test_htmlpage_change_view_popup_var_true(self):
        htmlpage = create_page()

        edit_page_url = reverse('admin:admin_edit_page', args=(htmlpage.pk, ))
        detail_page_url = '/page1/'

        change_url = reverse('admin:%s_%s_change' %('loosecms', 'htmlpage'), args=(htmlpage.pk, ))

        response = self.client.get(change_url, HTTP_REFERER=edit_page_url)
        self.assertEqual(response.context['is_popup'], True)

        response = self.client.get(change_url, HTTP_REFERER=detail_page_url)
        self.assertEqual(response.context['is_popup'], True)

    def test_htmlpage_change_view_popup_var_false(self):
        htmlpage = create_page()

        change_url = reverse('admin:%s_%s_change' %('loosecms', 'htmlpage'), args=(htmlpage.pk, ))
        changelist_url = reverse('admin:%s_%s_changelist' %('loosecms', 'htmlpage'))

        response = self.client.get(change_url)
        self.assertEqual(response.context['is_popup'], False)

        response = self.client.get(change_url, HTTP_REFERER=changelist_url)
        self.assertEqual(response.context['is_popup'], False)

    def test_response_add_get(self):
        add_url = reverse('admin:%s_%s_add' %('loosecms', 'htmlpage'))
        response = self.client.get(add_url)

        self.assertEqual(response.status_code, 200)

    def test_response_add_post_redirect_admin_urls(self):
        add_url = reverse('admin:%s_%s_add' %('loosecms', 'htmlpage'))
        changelist_url = reverse('admin:%s_%s_changelist' %('loosecms', 'htmlpage'))

        response = self.client.post(add_url, {'title': 'Page', 'slug': 'page'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(changelist_url, response.redirect_chain[0][0])

    def test_response_add_post_redirect_edit_page(self):
        add_url = reverse('admin:%s_%s_add' %('loosecms', 'htmlpage'))

        response = self.client.post(add_url, {'title': 'Page', 'slug': 'page', '_popup': True},
                                    follow=True)

        self.assertEqual(response.status_code, 200)

    def test_response_change_get(self):
        htmlpage = create_page()
        change_url = reverse('admin:%s_%s_change' %('loosecms', 'htmlpage'), args=(htmlpage.pk, ))
        response = self.client.get(change_url)

        self.assertEqual(response.status_code, 200)

    def test_response_add_post_redirect_admin_urls(self):
        htmlpage = create_page()
        change_url = reverse('admin:%s_%s_change' %('loosecms', 'htmlpage'), args=(htmlpage.pk, ))
        changelist_url = reverse('admin:%s_%s_changelist' %('loosecms', 'htmlpage'))

        response = self.client.post(change_url, {'title': 'Page', 'slug': 'page'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(changelist_url, response.redirect_chain[0][0])

    def test_response_add_post_redirect_edit_page(self):
        htmlpage = create_page()
        change_url = reverse('admin:%s_%s_change' %('loosecms', 'htmlpage'), args=(htmlpage.pk, ))

        response = self.client.post(change_url, {'title': 'Page', 'slug': 'page', '_popup': True},
                                    follow=True)

        self.assertEqual(response.status_code, 200)











