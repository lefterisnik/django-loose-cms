# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from .helpers import *


class AnonymousViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_no_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_edit_page(self):
        htmlpage = create_page()
        url = reverse('admin:admin_edit_page', args=(htmlpage.pk, ))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_edit_template_page(self):
        htmlpage = create_page(is_template=True)
        url = reverse('admin:admin_edit_page', args=(htmlpage.pk, ))

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_page(self):
        htmlpage = create_page()

        response = self.client.get('/page/')
        self.assertEqual(response.status_code, 200)

    def test_template_page(self):
        htmlpage = create_page(is_template=True)

        response = self.client.get('/page/')
        self.assertEqual(response.status_code, 404)

    def test_custom_error_page(self):
        self.custom_error_page = create_page(title='Page 404', is_error=True)
        response = self.client.get('/page/')
        self.assertEqual(response.context['page'].title, 'Page 404')


class StaffViews(TestCase):

    def setUp(self):
        self.client = Client()
        create_admin_user()

    def test_no_pages(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_page(self):
        htmlpage = create_page()
        self.client.login(username='admin', password='admin')

        response = self.client.get('/page/')
        self.assertEqual(response.status_code, 200)

    def test_template_page(self):
        htmlpage = create_page(is_template=True)
        self.client.login(username='admin', password='admin')

        response = self.client.get('/page/')
        self.assertEqual(response.status_code, 200)

    def test_custom_error_page(self):
        self.client.login(username='admin', password='admin')
        self.custom_error_page = create_page(is_error=True)

        response = self.client.get('/error/')
        self.assertTemplateUsed(response, 'admin/editor_form.html')

    def test_creation_page(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get('/page/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_slug'], 'page')

    def test_creation_page_multislug(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get('/page1/page2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_slug'], 'page1/page2')

    def test_deny_creation_page_under_specific_names(self):
        self.client.login(username='admin', password='admin')

        response = self.client.get('/admin/page/')
        self.assertEqual(response.status_code, 404)

    def test_multislug_page(self):
        self.client.login(username='admin', password='admin')
        htmlpage = create_page(slug='page1/page2')

        response = self.client.get('/page1/page2/')
        self.assertEqual(response.status_code, 200)




