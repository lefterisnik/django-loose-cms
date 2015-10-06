# -*- coding: utf-8 -*-
from ..plugin_pool import plugin_pool


def get_app_urls(embed_only=False):
    if embed_only:
        return plugin_pool.embed_urlpatterns
    else:
        return plugin_pool.extra_urlpatterns, plugin_pool.embed_urlpatterns
