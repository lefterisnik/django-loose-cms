"""Django Loose CMS default settings and validation test"""

from __future__ import absolute_import
from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured


__all__ = []

_DEFAULTS = {
    'CONSTANCE_BACKEND': 'constance.backends.database.DatabaseBackend',
    'CONSTANCE_CONFIG': {
        'SITE_TITLE': ('Site', _('Give the name of the site.')),
        'FAVICON': ('images/favicon.ico', _('Give the path of the site favicon.'))
    },
}

for key, value in list(_DEFAULTS.items()):
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except ImportError:
        pass

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

if 'constance.context_processors.config' not in context_processors:
    context_processors.append('constance.context_processors.config')

if 'bootstrap_admin' not in settings.INSTALLED_APPS:
    raise ImproperlyConfigured("Django Loose CMS requires 'bootstrap_admin' in 'INSTALLED_APPS'.")

if settings.INSTALLED_APPS.index('bootstrap_admin') > settings.INSTALLED_APPS.index('django.contrib.admin'):
    raise ImproperlyConfigured("Django Loose CMS requires 'boostrap_admin' to be before 'django.contrib.admin' in "
                               "'INTALLED_APPS'.")

if settings.INSTALLED_APPS.index('loosecms') > settings.INSTALLED_APPS.index('constance'):
    raise ImproperlyConfigured("Django Loose CMS requires 'loosecms' to be before 'constance' in ""
                               "'INTALLED_APPS'.")

