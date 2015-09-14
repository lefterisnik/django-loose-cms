# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from loosecms.models import HtmlPage, Row, Configuration
from django.contrib.sites.models import Site
from loosecms.views import error404


def create_page(is_template):
    htmlpage = HtmlPage.objects.create(title='page1',
                                       slug='page1',
                                       is_template=is_template)
    return htmlpage


def create_row_plugin(htmlpage):
    row = Row.objects.create(type='RowPlugin',
                             title='row1',
                             slug='row1',
                             page=htmlpage,
                             order=0)
    return row


def create_404_page():
    htmlpage = HtmlPage.objects.create(title='page404',
                                       slug='page404',
                                       is_error=True)
    return htmlpage


class AnonymousViews(TestCase):

    def setUp(self):
        self.client = Client()
        site = Site.objects.create(domain='example.com', name='example.com')
        site.save()
        configuration = Configuration.objects.create(site=site)
        configuration.save()

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
        site = Site.objects.create(domain='example.com', name='example.com')
        site.save()
        configuration = Configuration.objects.create(site=site)
        configuration.save()

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

    def test_page(self):
        """
        Test case of an anonymous user with pages in database to edit page
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
        response = self.client.get(row_url+'?type=RowPlugin')
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

    def test_custom_error_page(self):
        """
        Test case of an anonymous user with pages in database to get a non existing page
        Redirect to custom 404 if exists
        :return:
        """
        self.client.login(username='admin', password='admin')
        self.custom_error_page = create_404_page()
        response = self.client.get('/page1/')
        self.assertTemplateUsed(response, 'admin/editor_form.html')




