# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from loosecms.views import error404
from .helpers import *


class AnonymousViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_no_pages(self):
        """
        Test case of an anonymous user with no pages at database
        Redirect to the admin login page
        Simulate first experience after installation, give the chance to login and start playing with cms
        :return: 302 redirect
        """
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)

    def test_edit_page(self):
        """
        Test case of an anonymous user with pages in database to edit page
        Redirect to admin login page
        :return: 302 redirect
        """
        self.htmlpage = create_page(is_template=False)
        url = reverse('admin:admin_edit_page', args=(self.htmlpage.pk, ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_edit_template_page(self):
        """
        Test case of an anonymous user with pages in database to edit page
        #TODO: Deny access to edit the template with 404, TEMP: Redirect to login page
        :return: 302 redirect
        """
        self.htmlpage = create_page(is_template=True)
        url = reverse('admin:admin_edit_page', args=(self.htmlpage.pk, ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_page(self):
        """
        Test case of an anonymous user with pages in database
        Simulate page access
        :return: 200
        """
        self.htmlpage = create_page(is_template=False)
        response = self.client.get('/page1/')

        self.assertEqual(response.status_code, 200)

    def test_template_page(self):
        """
        Test case of an anonymous user with template pages in database
        Deny access with 404
        :return: 404
        """
        self.htmlpage = create_page(is_template=True)
        response = self.client.get('/page1/')

        self.assertEqual(response.status_code, 404)

    def test_custom_error_page(self):
        """
        Test case of an anonymous user with pages in database to get a non existing page
        Redirect to custom 404 if exists
        :return:
        """
        self.custom_error_page = create_404_page()
        response = self.client.get('/page1/')
        self.assertEqual(response.context['page'].title, 'page404')


class StaffViews(TestCase):

    def setUp(self):
        self.client = Client()
        get_user_model().objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='admin')

    def test_no_pages(self):
        """
        Test case of a staff user with no pages at database
        Allow access to home page
        Simulate first experience after installation, give the chance to create page the first page
        :return: 200
        """
        self.client.login(username='admin', password='admin')
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)

    def test_page(self):
        """
        Test case of an staff user with pages in database to view page
        Allow access
        :return: 200
        """
        self.htmlpage = create_page(is_template=False)
        self.client.login(username='admin', password='admin')
        response = self.client.get('/page1/')

        self.assertEqual(response.status_code, 200)

    def test_template_page(self):
        """
        Test case of a staff user with template pages in database
        Allow access to template page
        :return: 200
        """
        self.htmlpage = create_page(is_template=True)
        self.client.login(username='admin', password='admin')
        response = self.client.get('/page1/')

        self.assertEqual(response.status_code, 200)

    def test_custom_error_page(self):
        """
        Test case of an staff user with pages in database to get a non existing page
        Redirect to custom 404 if exists
        :return:
        """
        self.client.login(username='admin', password='admin')
        self.custom_error_page = create_404_page()
        response = self.client.get('/page1/')
        self.assertTemplateUsed(response, 'admin/editor_form.html')




