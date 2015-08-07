"""Django Loose CMS default settings and validation test"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    django_backend = [x for x in settings.TEMPLATES
                      if x['BACKEND'] == 'django.template.backends.django.DjangoTemplates'][0]
except IndexError:
    raise ImproperlyConfigured("Django Loose CMS requires django.template.context_processors.request in "
                               "'django.template.backends.django.DjangoTemplates' context processors.")

context_processors = django_backend.get('OPTIONS', {}).get('context_processors', [])
if ('django.core.context_processors.request' not in context_processors and
    'django.template.context_processors.request' not in context_processors):
    raise ImproperlyConfigured("Django Loose CMS requires django.template.context_processors.request in "
                               "'django.template.backends.django.DjangoTemplates' context processors.")

if 'loosecms.context_processors.global_settings' not in context_processors:
    context_processors.append('loosecms.context_processors.global_settings')

if 'bootstrap_admin' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured("Django Loose CMS requires 'bootstrap_admin' in 'INSTALLED_APPS'.")
elif settings.INSTALLED_APPS.index('bootstrap_admin') > settings.INSTALLED_APPS.index('django.contrib.admin'):
    raise ImproperlyConfigured("Django Loose CMS requires 'boostrap_admin' to be before 'django.contrib.admin' in "
                               "'INTALLED_APPS'.")