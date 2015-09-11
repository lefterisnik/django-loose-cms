# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.apps import SitesConfig
from django.core.exceptions import ObjectDoesNotExist
from django.db import ProgrammingError, OperationalError


class LooseCMSSiteConfig(SitesConfig):

    def ready(self):
        super(LooseCMSSiteConfig, self).ready()

        # Load configs from database
        Site = self.get_model('Site')
        try:
            current_site = Site.objects.get_current()
        except (ProgrammingError, OperationalError) as e:
            return
        except Site.DoesNotExist:
            raise ObjectDoesNotExist("In settings.py you set wrong SITE_ID. Please set the SITE_ID to match "
                                     "with these from database.")

        # TODO: think what we can do if values are deferrent. We must select which value we keep.
        # TODO: think what we can do about new policy of ckeditor from removing filebrowser. (todo image plugin)
        ckeditor_upload_path = getattr(settings, 'CKEDITOR_UPLOAD_PATH', None)
        if not ckeditor_upload_path and current_site.loosecmsconfiguration.ckeditor_upload_path:
            setattr(settings, 'CKEDITOR_UPLOAD_PATH', current_site.loosecmsconfiguration.ckeditor_upload_path)


