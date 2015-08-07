# -*- coding: utf-8 -*-
from django.conf import settings


def global_settings(request):
    return {
        'site_name': settings.LOOSECMS_SITE_NAME,
        'site_favicon': settings.LOOSECMS_SITE_FAVICON,
    }