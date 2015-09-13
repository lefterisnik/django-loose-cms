# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.core.exceptions import ImproperlyConfigured

from ckeditor.widgets import CKEditorWidget

LOOSECMS_DEFAULT_CONFIG = {
    'skin': 'moono',
    'toolbar': 'full',
    'height': '300',
    'width': 'auto',
    'filebrowserWindowWidth': 940,
    'filebrowserWindowHeight': 725,
}


class LoosecmsCKEditorWidget(CKEditorWidget):

    class Media(CKEditorWidget.Media):
        css = {
            'all': ('loosecms/loosecms/css/admin/ckeditor/ckeditor.css',),
        }

    def __init__(self, loosecms_plugins=None, *args, **kwargs):
        config_name = kwargs.pop('config_name', 'default')
        extra_plugins = kwargs.pop('extra_plugins', [])
        external_plugin_resources = kwargs.pop('external_plugin_resources', [])
        super(LoosecmsCKEditorWidget, self).__init__(*args, **kwargs)

        # Setup config from defaults.
        self.config = LOOSECMS_DEFAULT_CONFIG.copy()

        # Try to get valid config from settings.
        configs = getattr(settings, 'CKEDITOR_CONFIGS', None)
        if configs:
            if isinstance(configs, dict):
                # Make sure the config_name exists.
                if config_name in configs:
                    config = configs[config_name]
                    # Make sure the configuration is a dictionary.
                    if not isinstance(config, dict):
                        raise ImproperlyConfigured('CKEDITOR_CONFIGS["%s"] \
                                setting must be a dictionary type.' %
                                                   config_name)
                    # Override defaults with settings config.
                    self.config.update(config)
                else:
                    raise ImproperlyConfigured("No configuration named '%s' \
                            found in your CKEDITOR_CONFIGS setting." %
                                               config_name)
            else:
                raise ImproperlyConfigured('CKEDITOR_CONFIGS setting must be a\
                        dictionary type.')

        extra_plugins = extra_plugins or []

        if extra_plugins:
            self.config['extraPlugins'] = ','.join(extra_plugins)

        self.external_plugin_resources = external_plugin_resources or []
        self.extra_plugins = extra_plugins
        self.loosecms_plugins = loosecms_plugins

    def render(self, name, value, attrs=None):
        return self.pre_render(name, value, attrs) + super(LoosecmsCKEditorWidget, self).render(name, value, attrs)

    def pre_render(self, name, value, attrs=None):
        return mark_safe(render_to_string('ckeditor/widget_additional.html', {'plugins': self.loosecms_plugins}))

    def _set_config(self):
        if 'filebrowserUploadUrl' not in self.config:
            self.config.setdefault('filebrowserUploadUrl', reverse('ckeditor_upload'))
        if 'filebrowserBrowseUrl' not in self.config:
            self.config.setdefault('filebrowserBrowseUrl', reverse('ckeditor_browse'))
        super(LoosecmsCKEditorWidget, self)._set_config()
