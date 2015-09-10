# -*- coding: utf-8 -*-
import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def setup():
    """
    Django Loose CMS default settings and validation test
    """
    # Exam template backend
    try:
        django_backend = [x for x in settings.TEMPLATES
                          if x['BACKEND'] == 'django.template.backends.django.DjangoTemplates'][0]
    except IndexError:
        raise ImproperlyConfigured("Django Loose CMS requires 'django.template.backends.django.DjangoTemplates'"
                                   " as backend at template settings.")

    # Exam context processors
    context_processors = django_backend.get('OPTIONS', {}).get('context_processors', [])
    if ('django.core.context_processors.request' not in context_processors and
        'django.template.context_processors.request' not in context_processors):
        raise ImproperlyConfigured("Django Loose CMS requires django.template.context_processors.request in "
                                   "'django.template.backends.django.DjangoTemplates' context processors.")

    if 'loosecms.context_processors.global_settings' not in context_processors:
        raise ImproperlyConfigured("Django Looces CMS requires 'loosecms.context_processors.global_settings' in "
                                   "'django.template.backends.django.DjangoTemplates' context processors.")

    # Exam installed apps
    if 'bootstrap_admin' not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured("Django Loose CMS requires 'bootstrap_admin' in 'INSTALLED_APPS'.")
    elif settings.INSTALLED_APPS.index('bootstrap_admin') > settings.INSTALLED_APPS.index('django.contrib.admin'):
        raise ImproperlyConfigured("Django Loose CMS requires 'boostrap_admin' to be before 'django.contrib.admin' in "
                                   "'INTALLED_APPS'.")

    if 'ckeditor' not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured("Django Loose CMS requires 'ckeditor' in 'INSTALLED_APPS'.")
    elif settings.INSTALLED_APPS.index('ckeditor') > settings.INSTALLED_APPS.index('loosecms'):
        raise ImproperlyConfigured("Django Loose CMS requires 'ckeditor' to be before 'loosecms' in 'INSTALLED_APPS'.")

    if 'django.contrib.humanize' not in settings.INSTALLED_APPS:
        raise ImproperlyConfigured("Django Loose CMS requires 'django.contrib.humanize' in 'INSTALLED_APPS'.")

    # Exam if media url/root exists
    media_url = getattr(settings, 'MEDIA_URL', None)
    if not media_url:
        raise ImproperlyConfigured("Djanog Loose CMS requires 'MEDIA_URL' setting.")

    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if not media_root:
        raise ImproperlyConfigured("Django Loose CMS requires 'MEDIA_ROOT' setting.")
