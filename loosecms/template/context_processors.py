# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site


def global_settings(request):
    configuration = dict()
    try:
        current_site = get_current_site(request)
    except ObjectDoesNotExist:
        return configuration

    configuration.update(
        site=current_site,
    )

    try:
        loosecms_configuration = current_site.configuration
        configuration.update(
            loosecms=loosecms_configuration,
        )
    except ObjectDoesNotExist:
        pass

    # Clear cache for the next time
    Site.objects.clear_cache()
    return configuration