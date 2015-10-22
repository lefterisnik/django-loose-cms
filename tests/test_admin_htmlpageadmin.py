# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from loosecms.models import *
from .helpers import *



class AdminPageViews(TestCase):

    def setUp(self):
        self.client = Client()
        create_admin_user()
        self.client.login(username='admin', password='admin')

    ##
    ## Test access to edit views for normal and template pages
    ##

    def test_edit_page(self):
        htmlpage = create_page()
        url = reverse('admin:admin_edit_page', args=(htmlpage.pk, ))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_template_page(self):
        htmlpage = create_page(is_template=True)
        url = reverse('admin:admin_edit_page', args=(htmlpage.pk, ))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    ##
    ## Test add, edit, delete, remove plugin urls
    ##

    def test_edit_template_page_add_plugin(self):
        htmlpage = create_page()
        add_placeholder_url = reverse('admin:admin_add_placeholder', args=(htmlpage.pk, ))
        add_plugin_url = reverse('admin:admin_add_plugin')

        # Testing add row plugin form
        response = self.client.get(add_placeholder_url, {'type': 'RowPlugin'})
        self.assertEqual(response.status_code, 200)

        # Testing add row post action
        response = self.client.post(add_plugin_url, {'type': 'RowPlugin', 'title': 'Row',
                                                     'slug': 'row', 'page': htmlpage.pk,
                                                     'order': 0, '_popup': True})
        self.assertEqual(response.status_code, 200)

        row = Row.objects.get(title='Row')
        self.assertEqual(row.page, htmlpage)
        self.assertEqual(row.type, 'RowPlugin')

        # Testing add column plugin form
        response = self.client.get(add_plugin_url, {'type': 'ColumnPlugin', 'placeholder': row.pk})
        self.assertEqual(response.status_code, 200)

        # Testing add column post action
        response = self.client.post(add_plugin_url, {'type': 'ColumnPlugin', 'placeholder': row.pk,
                                                     'title': 'Column', 'slug': 'column',
                                                     'width': 12, 'order': 0, '_popup': True})
        self.assertEqual(response.status_code, 200)

        column = Column.objects.get(title='Column')
        self.assertEqual(column.placeholder.pk, row.pk)
        self.assertEqual(column.type, 'ColumnPlugin')

    def test_edit_template_page_remove_plugin(self):
        htmlpage = create_page()
        row = create_row_plugin(htmlpage)
        column = create_column_plugin(row)
        remove_plugin_url = reverse('admin:admin_remove_plugin', args=(column.pk, ))

        response = self.client.delete(remove_plugin_url)
        column = Column.objects.get(title='Column')
        self.assertEqual(column.placeholder, None)

    def test_edit_template_page_edit_delete_move_plugin(self):
        htmlpage = create_page()
        row = create_row_plugin(htmlpage)

        # Test edit row plugin
        edit_plugin_url = reverse('admin:admin_edit_plugin', args=(row.pk, ))
        response = self.client.get(edit_plugin_url)
        self.assertEqual(response.status_code, 200)

        # Testing delete row plugin
        delete_plugin_url = reverse('admin:admin_delete_plugin', args=(row.pk, ))
        response = self.client.get(delete_plugin_url)
        self.assertEqual(response.status_code, 200)

        # Testing move row plugin
        move_plugin_url = reverse('admin:admin_move_plugin', args=(row.pk, ))
        response = self.client.get(move_plugin_url)
        self.assertEqual(response.status_code, 200)

    ##
    ## Test popup variable
    ##

    def test_htmlpage_add_view_popup_var_true(self):
        htmlpage = create_page()
        add_page_url = reverse('admin:loosecms_htmlpage_add')
        edit_page_url = reverse('admin:admin_edit_page', args=(htmlpage.pk, ))
        detail_page_url = '/page/'

        response = self.client.get(add_page_url, HTTP_REFERER=edit_page_url)
        self.assertEqual(response.context['is_popup'], True)

        response = self.client.get(add_page_url, HTTP_REFERER=detail_page_url)
        self.assertEqual(response.context['is_popup'], True)

    def test_htmlpage_add_view_popup_var_false(self):
        add_page_url = reverse('admin:loosecms_htmlpage_add')
        changelist_page_url = reverse('admin:loosecms_htmlpage_changelist')

        response = self.client.get(add_page_url)
        self.assertEqual(response.context['is_popup'], False)

        response = self.client.get(add_page_url, HTTP_REFERER=changelist_page_url)
        self.assertEqual(response.context['is_popup'], False)

    def test_htmlpage_change_view_popup_var_true(self):
        htmlpage = create_page()
        change_page_url = reverse('admin:loosecms_htmlpage_change', args=(htmlpage.pk, ))
        edit_page_url = reverse('admin:admin_edit_page', args=(htmlpage.pk, ))
        detail_page_url = '/page/'

        response = self.client.get(change_page_url, HTTP_REFERER=edit_page_url)
        self.assertEqual(response.context['is_popup'], True)

        response = self.client.get(change_page_url, HTTP_REFERER=detail_page_url)
        self.assertEqual(response.context['is_popup'], True)

    def test_htmlpage_change_view_popup_var_false(self):
        htmlpage = create_page()
        change_page_url = reverse('admin:loosecms_htmlpage_change', args=(htmlpage.pk, ))
        changelist_page_url = reverse('admin:loosecms_htmlpage_changelist')

        response = self.client.get(change_page_url)
        self.assertEqual(response.context['is_popup'], False)

        response = self.client.get(change_page_url, HTTP_REFERER=changelist_page_url)
        self.assertEqual(response.context['is_popup'], False)

    ##
    ## Test overriding modeladmin methods
    ##

    def test_response_add_get(self):
        add_page_url = reverse('admin:loosecms_htmlpage_add')

        response = self.client.get(add_page_url)
        self.assertEqual(response.status_code, 200)

    def test_response_add_post_redirect_admin_urls(self):
        add_page_url = reverse('admin:loosecms_htmlpage_add')
        changelist_page_url = reverse('admin:loosecms_htmlpage_changelist')

        response = self.client.post(add_page_url, {'title': 'Page', 'slug': 'page'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(changelist_page_url, response.redirect_chain[0][0])

    def test_response_add_post_redirect_edit_page(self):
        add_page_url = reverse('admin:loosecms_htmlpage_add')

        response = self.client.post(add_page_url, {'title': 'Page', 'slug': 'page', '_popup': True},
                                    follow=True)
        self.assertEqual(response.status_code, 200)

    def test_response_change_get(self):
        htmlpage = create_page()
        change_page_url = reverse('admin:loosecms_htmlpage_change', args=(htmlpage.pk, ))

        response = self.client.get(change_page_url)
        self.assertEqual(response.status_code, 200)

    def test_response_change_post_redirect_admin_urls(self):
        htmlpage = create_page()
        change_page_url = reverse('admin:loosecms_htmlpage_change', args=(htmlpage.pk, ))
        changelist_page_url = reverse('admin:loosecms_htmlpage_changelist')

        response = self.client.post(change_page_url, {'title': 'Page', 'slug': 'page'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(changelist_page_url, response.redirect_chain[0][0])

    def test_response_change_post_redirect_edit_page(self):
        htmlpage = create_page()
        change_page_url = reverse('admin:loosecms_htmlpage_change', args=(htmlpage.pk, ))

        response = self.client.post(change_page_url, {'title': 'Page', 'slug': 'page', '_popup': True},
                                    follow=True)
        self.assertEqual(response.status_code, 200)










