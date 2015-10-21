# -*- coding: utf-8 -*-
from django.core.urlresolvers import get_resolver
from ..plugin_pool import plugin_pool


def get_app_urls(embed_only=False):
    if embed_only:
        return plugin_pool.embed_urlpatterns
    else:
        return plugin_pool.extra_urlpatterns, plugin_pool.embed_urlpatterns


def get_patterns():
    resolver = get_resolver(None)
    patterns = []
    for key, value in resolver.reverse_dict.items():
        split_value = value[0][0][0].split('/')[0]
        if not split_value.startswith('%') and split_value not in patterns and split_value != '':
            patterns.append(split_value)

    if 'admin' not in patterns:
        patterns.append('admin')

    return patterns
