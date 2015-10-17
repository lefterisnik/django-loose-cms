# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import Client, TestCase, override_settings, modify_settings
from django.utils import translation
from loosecms.models import HtmlPage
from .helpers import *


class TestSimpleLocaleMiddleware(TestCase):

    def setUp(self):
        self.client = Client()
        self.htmlpage = HtmlPage.objects.create(title='Page', home=True)

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

    @override_settings(LANGUAGE_CODE='el')
    def test_process_request_without_urls_el_no_session(self):
        with self.modify_settings(MIDDLEWARE_CLASSES={
            'append': 'loosecms.middleware.locale.SimpleLocaleMiddleware',
        }):
            # Test if default language that activates middleware is LANGUAGE_CODE
            # and not user request language priority
            response = self.client.get('/')
            self.assertEqual(translation.get_language(), 'el')
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

    @override_settings(LANGUAGE_CODE='el')
    def test_process_request_without_urls_el_session(self):
        with self.modify_settings(MIDDLEWARE_CLASSES={
            'append': 'loosecms.middleware.locale.SimpleLocaleMiddleware',
        }):
            # Test if user set session language to be activated from middleware
            response = self.client.get('/')
            self.assertEqual(translation.get_language(), 'el')
            self.assertEqual(response.status_code, 200)

            session = self.client.session
            session[translation.LANGUAGE_SESSION_KEY] = 'en'
            session.save()
            response = self.client.get('/')
            self.assertEqual(translation.get_language(), 'en')
            self.assertEqual(response.status_code, 200)

'''@override_settings(ROOT_URLCONF='tests.urls')
class TestSimplepatternsen(TestCase):

    def setUp(self):
        self.client = Client()
        self.htmlpage = HtmlPage.objects.create(title='Page', home=True)

    @modify_settings(MIDDLEWARE_CLASSES={
        'append': 'loosecms.middleware.locale.SimpleLocaleMiddleware',
    })
    @override_settings(LANGUAGE_CODE='en')
    def test_process_request_with_urls_en_no_session(self):
        # Test if default language that activates middleware is LANGUAGE_CODE or url
        # and not user request language priority
        print "to gnwsto"
        response1 = self.client.get('/', follow=True)

        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response1.status_code, 200)

        response3 = self.client.get('/en/')
        self.assertEqual(response3.status_code, 404)

        response2 = self.client.get('/el/')
        self.assertEqual(translation.get_language(), 'el')
        self.assertEqual(response2.status_code, 200)



    @modify_settings(MIDDLEWARE_CLASSES={
        'append': 'loosecms.middleware.locale.SimpleLocaleMiddleware',
    })
    @override_settings(LANGUAGE_CODE='en')
    def test_process_request_with_urls_en_session(self):
        # Test if user set session language activating from middleware
        response = self.client.get('/')
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.status_code, 200)

        session = self.client.session
        session[translation.LANGUAGE_SESSION_KEY] = 'el'
        session.save()

        response = self.client.get('/')
        self.assertEqual(translation.get_language(), 'el')
        self.assertRedirects(response, '/el/')'''

@override_settings(ROOT_URLCONF='tests.urls')
class TestSimplepatternsel(TestCase):

    def setUp(self):
        self.client = Client()
        self.htmlpage = HtmlPage.objects.create(title='Page', home=True)

    @modify_settings(MIDDLEWARE_CLASSES={
        'append': 'loosecms.middleware.locale.SimpleLocaleMiddleware',
    })
    @override_settings(LANGUAGE_CODE='el')
    def test_process_request_with_urls_el_no_session(self):
        # Test if default language that activates middleware is LANGUAGE_CODE or url
        # and not user request language priority
        response = self.client.get('/')

        self.assertEqual(translation.get_language(), 'el')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/en/')
        self.assertEqual(translation.get_language(), 'en')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/el/')
        self.assertEqual(response.status_code, 404)

    @modify_settings(MIDDLEWARE_CLASSES={
        'append': 'loosecms.middleware.locale.SimpleLocaleMiddleware',
    })
    @override_settings(LANGUAGE_CODE='el')
    def test_process_request_with_urls_el_session(self):
        # Test if user set session language activating from middleware
        response = self.client.get('/')
        self.assertEqual(translation.get_language(), 'el')
        self.assertEqual(response.status_code, 200)

        session = self.client.session
        session[translation.LANGUAGE_SESSION_KEY] = 'en'
        session.save()

        response = self.client.get('/')
        self.assertEqual(translation.get_language(), 'en')
        self.assertRedirects(response, '/en/')


