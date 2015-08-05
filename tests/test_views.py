# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from loosecms.models import HtmlPage, RowManager


class TestNoPageViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_no_pages_anonymous_user(self):
        """
        Test case of an anonymous user with no pages at database
        Redirect to the admin login page
        Simulate first experience after installation, give the chance to login and start playing with cms
        :return: 302 redirect
        """
        response = self.client.get('/')

        self.assertEqual(response.status_code, 302)

    def test_no_pages_staff_user(self):
        """
        Test case of a staff user with no pages at database
        Allow access to home page
        Simulate first experience after installation, give the chance to create page the first page
        :return: 200
        """
        User.objects.create_superuser(username='admin',
                                      email='admin@admin.com',
                                      password='admin')

        self.client.login(username='admin', password='admin')
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)


class TestHtmlPageAnomymousViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.htmlpage = HtmlPage.objects.create(title='page1',
                                           slug='page1',
                                           type='0')

    def test_edit_page_anonymous_user_authorize(self):
        """
        Test case of an anonymous user with pages in database to edit page
        Redirect to admin login page
        :return: 302 redirect
        """
        url = reverse('admin:admin_edit_page', args=(self.htmlpage.pk, ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_page_anonymous_user_authorize(self):
        """
        Test case of an anonymous user with pages in database
        Simulate page access
        :return: 200
        """
        response = self.client.get('/page1/')

        self.assertEqual(response.status_code, 200)


class TestHtmlPageStaffViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.htmlpage = HtmlPage.objects.create(title='page1',
                                           slug='page1',
                                           type='0')
        self.user = User.objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='admin')

    def test_edit_page_staff_user_authorize(self):
        """
        Test case of a staff user with pages in database
        Allow access, to build the page
        :return: 200
        """
        self.client.login(username='admin', password='admin')
        url = reverse('admin:admin_edit_page', args=(self.htmlpage.pk, ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_page_staff_user_authorize(self):
        """
        Test case of an anonymous user with pages in database to edit page
        Allow access
        :return: 200
        """
        self.client.login(username='admin', password='admin')
        response = self.client.get('/page1/')

        self.assertEqual(response.status_code, 200)


class TestTemplateHtmlPageAnonymousViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.htmlpage = HtmlPage.objects.create(title='page1',
                                           slug='page1',
                                           type='0',
                                           is_template=True)

    def test_template_page_anonymous_user_authorize(self):
        """
        Test case of an anonymous user with template pages in database
        Deny access with 404
        :return: 404
        """
        response = self.client.get('/page1/')

        self.assertEqual(response.status_code, 404)

    def test_edit_template_page_anonymous_user_authorize(self):
        """
        Test case of an anonymous user with pages in database to edit page
        #TODO: Deny access to edit the template with 404, TEMP: Redirect to login page
        :return: 302 redirect
        """
        url = reverse('admin:admin_edit_page', args=(self.htmlpage.pk, ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)


class TestTemplateHtmlPageStaffViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.htmlpage = HtmlPage.objects.create(title='page1',
                                           slug='page1',
                                           type='0',
                                           is_template=True)
        self.user = User.objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='admin')

    def test_template_page_staff_user_authorize(self):
        """
        Test case of a staff user with template pages in database
        Allow access to template page
        :return: 200
        """
        self.client.login(username='admin', password='admin')
        response = self.client.get('/page1/')

        self.assertEqual(response.status_code, 200)

    def test_edit_template_page_staff_user_authorize(self):
        """
        Test case of a staff user with pages in database to edit page
        Allow access to edit template
        :return: 200
        """
        self.client.login(username='admin', password='admin')
        url = reverse('admin:admin_edit_page', args=(self.htmlpage.pk, ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_edit_template_page_add_plugin_staff_user_authorize(self):
        """
        Test case of a staff user with pages in database to add plugin at edit page
        Allow access to edit template
        :return: 200
        """
        self.client.login(username='admin', password='admin')
        url = reverse('admin:admin_add_plugin', args=(self.htmlpage.pk, ))
        response = self.client.get(url+'?type=RowPlugin')

        self.assertEqual(response.status_code, 200)

# TODO: Add test at edit style of plugin
class TestTemplateHtmlPageRowPluginStaffViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.htmlpage = HtmlPage.objects.create(title='page1',
                                           slug='page1',
                                           type='0',
                                           is_template=True)
        self.row = RowManager.objects.create(type='RowPlugin',
                                             title='row1',
                                             slug='row1',
                                             page=self.htmlpage,
                                             order=0)
        self.user = User.objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='admin')

    def test_edit_template_page_edit_plugin_staff_user_authorize(self):
        """
        Test case of a staff user with template pages in database to edit plugin
        Allow access to edit plugin
        :return: 200
        """
        self.client.login(username='admin', password='admin')
        url = reverse('admin:admin_edit_plugin', args=(self.htmlpage.pk, self.row.pk))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_edit_template_page_delete_plugin_staff_user_authorize(self):
        """
        Test case of a staff user with pages in database to delete plugin
        Allow access to delete plugin
        :return: 200
        """
        self.client.login(username='admin', password='admin')
        url = reverse('admin:admin_delete_plugin', args=(self.htmlpage.pk, self.row.pk))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_edit_template_page_move_plugin_staff_user_authorize(self):
        """
        Test case of a staff user with pages in database to move plugin
        Allow access to move plugin
        :return: 200
        """
        self.client.login(username='admin', password='admin')
        url = reverse('admin:admin_move_plugin', args=(self.htmlpage.pk, self.row.pk))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)




