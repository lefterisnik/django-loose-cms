# -*- coding: utf-8 -*-
import os
from dynamic_preferences.types import StringPreference, ChoicePreference
from dynamic_preferences import user_preferences_registry, global_preferences_registry
from django.conf import settings

# We start with a global preference
@global_preferences_registry.register
class SiteTitle(StringPreference):
    name = 'site_title'
    default = 'My site'

@global_preferences_registry.register
class Favicon(ChoicePreference):
    name = 'favicon'

    if settings.MEDIA_ROOT:
        try:
            choices = (('images/%s' %i, 'images/%s' %i) for i in os.listdir(os.path.join(settings.MEDIA_ROOT, 'images')))
        except OSError:
            choices = (('images/favicon.ico', 'images/favicon.ico'),)

    default = 'images/favicon.ico'