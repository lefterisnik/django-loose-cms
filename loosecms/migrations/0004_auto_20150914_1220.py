# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import loosecms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('loosecms', '0003_remove_loosecmsconfiguration_ckeditor_upload_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('favicon', loosecms.fields.UploadFilePathField(path=b'images', verbose_name='favicon', recursive=True, upload_to=b'images')),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configurations',
            },
        ),
        migrations.RemoveField(
            model_name='loosecmsconfiguration',
            name='site',
        ),
        migrations.DeleteModel(
            name='LooseCMSConfiguration',
        ),
    ]
