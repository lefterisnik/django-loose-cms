# -*- coding: utf-8 -*-
import unittest
from django.test import Client
from django.contrib.auth.models import User


class TestViews(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_no_pages_anonymous_user(self):
        """
        Test case of an anonymous user with no pages at database redirection to the admin login page
        Simulate first experience after installation
        :return: 302 redirect
        """
        response = self.client.get('/')

        if response.wsgi_request.user.is_anonymous():
            self.assertEqual(response.status_code, 302)

    def test_no_pages_login_staff_user(self):
        """
        Test case of an anonymous user with no pages at database redirection to the admin login page
        Simulate first experience after installation
        :return: 302 redirect
        """
        user = User.objects.create_superuser(username='admin', email='admin@admin.com', password='admin')
        self.client.login(username='admin', password='admin')
        response = self.client.get('/')

        if response.wsgi_request.user.is_authenticated():
            self.assertEqual(response.status_code, 200)