# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.apps import SitesConfig


class LooseCMSSiteConfig(SitesConfig):

    def ready(self):
        super(LooseCMSSiteConfig, self).ready()

        # Load configs from database
        Site = self.get_model('Site')
        current_site = Site.objects.get_current()

        # TODO: think what we can do if values are deferrent. We must select which value we keep.
        # TODO: think what we can do about new policy of ckeditor from removing filebrowser. (todo image plugin)
        ckeditor_upload_path = getattr(settings, 'CKEDITOR_UPLOAD_PATH', None)
        if not ckeditor_upload_path and current_site.loosecmsconfiguration.ckeditor_upload_path:
            setattr(settings, 'CKEDITOR_UPLOAD_PATH', current_site.loosecmsconfiguration.ckeditor_upload_path)


