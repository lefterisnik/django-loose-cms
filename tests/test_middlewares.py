# -*- coding: utf-8 -*-
from django.test import Client, TestCase, override_settings, modify_settings
from django.utils import translation
from .helpers import *


class TestSimpleLocaleMiddleware(TestCase):

    def setUp(self):
        self.client = Client()
        self.htmlpage = create_page(home=True)

    @override_settings(LANGUAGE_CODE='en')
    def test_process_request_without_urls_en_no_session(self):
        with self.modify_settings(MIDDLEWARE_CLASSES={
            'append': 'loosecms.middleware.locale.SimpleLocaleMiddleware',
        }):
            # Test if default language that activates middleware is LANGUAGE_CODE
            # and not user request language priority
            response = self.client.get('/')
            self.assertEqual(translation.get_language(), 'en')
            self.assertEqual(response.status_code, 200)

    @override_settings(LANGUAGE_CODE='en')
    def test_process_request_without_urls_en_session(self):
        with self.modify_settings(MIDDLEWARE_CLASSES={
            'append': 'loosecms.middleware.locale.SimpleLocaleMiddleware',
        }):
            # Test if user set session language to be activated from middleware
            response = self.client.get('/')
            self.assertEqual(translation.get_language(), 'en')
            self.assertEqual(response.status_code, 200)

            session = self.client.session
            session[translation.LANGUAGE_SESSION_KEY] = 'el'
            session.save()
            response = self.client.get('/')
            self.assertEqual(translation.get_language(), 'el')
            self.assertEqual(response.status_code, 200)

@override_settings(ROOT_URLCONF='tests.urls')
class TestSimplepatternsel(TestCase):

    def setUp(self):
        self.client = Client()
        self.htmlpage = create_page(home=True)

    @modify_settings(MIDDLEWARE_CLASSES={
        'append': 'loosecms.middleware.locale.SimpleLocaleMiddleware',
    })
    @override_settings(LANGUAGE_CODE='en')
    def test_process_request_with_urls_el_no_session(self):
        # Test if default language that activates middleware is LANGUAGE_CODE or url
        # and not user request language priority
        response = self.client.get('/')

        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/el/')
        self.assertEqual(translation.get_language(), 'el')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 404)

    @modify_settings(MIDDLEWARE_CLASSES={
        'append': 'loosecms.middleware.locale.SimpleLocaleMiddleware',
    })
    @override_settings(LANGUAGE_CODE='en')
    def test_process_request_with_urls_el_session(self):
        # Test if user set session language activating from middleware
        response = self.client.get('/')
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.status_code, 200)

        session = self.client.session
        session[translation.LANGUAGE_SESSION_KEY] = 'el'
        session.save()

        response = self.client.get('/')
        self.assertEqual(translation.get_language(), 'el')
        self.assertRedirects(response, '/el/')


