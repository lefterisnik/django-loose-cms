# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.contrib.auth import get_user_model


class TestSiteFilemanager(TestCase):

    def setUp(self):
        self.client = Client()
        get_user_model().objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='admin')

    def test_anonymous_access(self):
        response = self.client.get('/admin/filemanager/')

        self.assertEqual(response.status_code, 302)

    def test_staff_access(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/admin/filemanager/')

        self.assertEqual(response.status_code, 200)
