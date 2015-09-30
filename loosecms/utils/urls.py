# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.importlib import import_module


def get_app_urls(embed_only=False):
    # Find all urlconfs of all plugins
    modname = 'urls'
    extra_urlpatterns = []
    embed_urlpatterns = []

    for app in settings.INSTALLED_APPS:
        try:
            if 'loosecms_' in app:
                module_name = '%s.%s' %(app, modname)
                module = import_module(module_name)
                if not embed_only:
                    try:
                        extra_urlpatterns += module.urlpatterns
                    except Exception, e:
                        # urlpatterns is not defined
                        pass

                try:
                    embed_urlpatterns += module.embed_urlpatterns
                except Exception,e:
                    # embed_urlpatterns is not defined
                    pass
        except Exception, e:
            continue

    if embed_only:
        return embed_urlpatterns
    else:
        return extra_urlpatterns, embed_urlpatterns


