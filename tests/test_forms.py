# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.test import Client, TestCase
from loosecms.fields import *
from loosecms.plugin_modeladmin import PluginModelAdmin
from loosecms.plugin_pool import plugin_pool


class Test(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title


class TestPlugin(PluginModelAdmin):
    model = Test
    name = 'Text'
    plugin_cke = True


class TestLoosecmsRTField(TestCase):

    def test_rtf_form_field(self):
        model_field = LoosecmsRichTextField()
        form_field = model_field.formfield()
        self.assertIsInstance(form_field, LoosecmsRichTextFormField)

    def test_appending_plugins(self):
        model_field = LoosecmsRichTextField()
        plugin_pool.register_plugin(TestPlugin)
        form_field = model_field.formfield()
        self.assertIn('loosecms', form_field.extra_plugins)


class TestLoosecmsTaggableManager(TestCase):

    def test_taggable_manager_form_field(self):
        model_field = LoosecmsTaggableManager()
        form_field = model_field.formfield()
        self.assertIsInstance(form_field, LoosecmsTagField)


class TestUploadFilePathField(TestCase):

    def test_get_prep_value(self):
        model_field1 = UploadFilePathField()
        model_field2 = UploadFilePathField()
        model_field3 = UploadFilePathField()

        filepath = '/%s/test_forms.py' % settings.MEDIA_ROOT
        if model_field1.get_prep_value(filepath).startswith('/'):
            self.fail('Model field return value which starts with /.')

        filepath = None
        self.assertEqual(model_field2.get_prep_value(filepath), None)

        filepath = settings.MEDIA_ROOT + 'test_forms.py'
        self.assertNotIn(settings.MEDIA_ROOT, model_field3.get_prep_value(filepath))


    def test_upload_filepath_path_form_field(self):
        model_field = UploadFilePathField()
        form_field = model_field.formfield()
        self.assertIsInstance(form_field, UploadFilePathFormField)




