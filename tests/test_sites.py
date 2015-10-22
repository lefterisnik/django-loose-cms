# -*- coding: utf-8 -*-
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile


class TestSiteFilemanager(TestCase):
    """
    Exam when we open the filemanager in a new window. What we want to do. To upload files in
    storage, because upload_to is not defined
    """
    def setUp(self):
        self.client = Client()
        get_user_model().objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='admin')

    def test_anonymous_access(self):
        response = self.client.get('/admin/filemanager/')

        self.assertEqual(response.status_code, 302)

    def test_staff_get(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/admin/filemanager/')

        self.assertEqual(response.status_code, 200)

    def test_staff_get_context(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/admin/filemanager/', {'upload_to': 'upload'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['upload_to'], 'upload')

    def test_staff_post_no_files(self):
        self.client.login(username='admin', password='admin')
        response = self.client.post('/admin/filemanager/', {'upload_to': 'upload'})

        self.assertIn('id_document', response.context['errors'])
        self.assertEqual(response.status_code, 200)

    def test_staff_post_files(self):
        file_ = ContentFile('test file')
        file_.name = 'Test File'
        self.client.login(username='admin', password='admin')
        response = self.client.post('/admin/filemanager/', {'upload_to': 'upload', 'document': file_})

        self.assertIn('docs', response.context)
        self.assertEqual(response.status_code, 200)
