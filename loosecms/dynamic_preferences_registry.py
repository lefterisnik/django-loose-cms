# -*- coding: utf-8 -*-
from django import forms
from dynamic_preferences.types import BooleanPreference, StringPreference
from dynamic_preferences import user_preferences_registry, global_preferences_registry

# We start with a global preference
@global_preferences_registry.register
class SiteTitle(StringPreference):
    name = 'site_title'
    default = 'My site'

@global_preferences_registry.register
class Favicon(BooleanPreference):
    name = 'favicon'
    default = False
    widget = forms.FilePathField(path='media', match="\.ico$")