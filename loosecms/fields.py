# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .widgets import UploadFilePathWidget
import os
import re


class UploadFilePathField(models.FilePathField):
    description = _('Select or upload a file')

    def __init__(self, verbose_name=None, name=None, upload_to='', **kwargs):
        self.upload_to = upload_to
        super(UploadFilePathField, self).__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UploadFilePathField, self).deconstruct()
        if self.upload_to is not None:
            kwargs['upload_to'] = self.upload_to
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {
            'form_class': UploadFilePathFormField,
            'upload_to': self.upload_to,
        }
        defaults.update(kwargs)
        return super(UploadFilePathField, self).formfield(**defaults)


## Form Fields


class UploadFilePathFormField(forms.FilePathField):
    widget = UploadFilePathWidget

    def __init__(self, upload_to, *args, **kwargs):
        self.upload_to = upload_to
        self.path = kwargs.pop('path', '')
        self.path = os.path.join(settings.MEDIA_ROOT, self.path)

        super(UploadFilePathFormField, self).__init__(path=self.path, *args, **kwargs)
        self.widget.upload_to = self.upload_to

