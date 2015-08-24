# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.conf import settings
from .widgets import UploadFilePathWidget
from django.core.files.storage import default_storage
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.files import FieldFile, FileDescriptor
import os


class UploadFilePathField(models.FilePathField):
    attr_class = FieldFile
    descriptor_class = FileDescriptor
    description = _('Select or upload a file')

    def __init__(self, verbose_name=None, name=None, recursive=True, upload_to='', storage=None, **kwargs):
        self.upload_to, self.recursive = upload_to, recursive
        self.storage = storage or default_storage
        super(UploadFilePathField, self).__init__(verbose_name, name, recursive=recursive, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(UploadFilePathField, self).deconstruct()
        if self.upload_to is not None:
            kwargs['upload_to'] = self.upload_to
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super(UploadFilePathField, self).contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, self.descriptor_class(self))

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        value = os.path.join(settings.MEDIA_ROOT, value)
        return value

    def get_prep_value(self, value):
        value = super(UploadFilePathField, self).get_prep_value(value)
        if value is None:
            return None
        value = value.replace(settings.MEDIA_ROOT, '')
        if value.startswith('/'):
            value = value.lstrip('/')
        return value

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
        self.widget.path = self.path
        self.path = os.path.join(settings.MEDIA_ROOT, self.path)
        super(UploadFilePathFormField, self).__init__(path=self.path, *args, **kwargs)

        self.widget.upload_to = self.upload_to


