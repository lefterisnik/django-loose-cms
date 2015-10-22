# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib import admin
from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from loosecms.fields import *
from .helpers import *


'''class TestRTfield(models.Model):
    title = models.CharField(max_length=100)
    body = LoosecmsRichTextField()

    def __unicode__(self):
        return self.title

admin.site.register(TestRTfield)'''


class TestLoosecmsRTField(TestCase):

    def test_rtf_form_field(self):
        model_field = LoosecmsRichTextField()
        form_field = model_field.formfield()
        self.assertIsInstance(form_field, LoosecmsRichTextFormField)


class TestLoosecmsTaggableManager(TestCase):

    def test_taggable_manager_form_field(self):
        model_field = LoosecmsTaggableManager()
        form_field = model_field.formfield()
        self.assertIsInstance(form_field, LoosecmsTagField)


class TestUploadFilePathField(TestCase):

    def test_get_prep_value(self):
        model_field = UploadFilePathField()
        filepath = settings.MEDIA_ROOT + 'test_forms.py'
        self.assertNotIn(settings.MEDIA_ROOT, model_field.get_prep_value(filepath))


    def test_upload_filepath_path_form_field(self):
        model_field = UploadFilePathField()
        form_field = model_field.formfield()
        self.assertIsInstance(form_field, UploadFilePathFormField)




