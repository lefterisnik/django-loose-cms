# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns
from ...middleware.locale import NoPrefixLocaleRegexURLResolver

def simple_i18n_patterns(prefix, *args):
    """
    Adds the language code prefix to every URL pattern within this
    function, when the language not is the main language.
    This may only be used in the root URLconf, not in an included URLconf.
    """
    pattern_list = [prefix] + list(args)
    if not settings.USE_I18N:
        return pattern_list
    return [NoPrefixLocaleRegexURLResolver(pattern_list)]