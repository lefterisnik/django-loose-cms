# -*- coding: utf-8 -*-
"""Django Loose CMS default settings"""

from __future__ import absolute_import
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

__all__ = []

_DEFAULTS = {
    'CONSTANCE_CONFIG': {
        'SITE_TITLE': ('Site', _('Give the name of the site.')),
        'FAVICON': ('images/favicon.ico', _('Give the path of the site favicon.'))
    },
    'CONSTANCE_BACKEND': 'constance.backends.database.DatabaseBackend',
}

for key, value in list(_DEFAULTS.items()):
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except ImportError:
        pass
