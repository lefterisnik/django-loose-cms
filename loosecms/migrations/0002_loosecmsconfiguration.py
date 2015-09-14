# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import loosecms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('loosecms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LooseCMSConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('favicon', loosecms.fields.UploadFilePathField(path=b'images', verbose_name='favicon', recursive=True, upload_to=b'images')),
                ('ckeditor_upload_path', models.CharField(default=b'images', max_length=100, verbose_name='ckeditor upload path')),
                ('site', models.OneToOneField(to='sites.Site')),
            ],
            options={
                'verbose_name': 'Loose CMS Configuration',
                'verbose_name_plural': 'Loose CMS Configurations',
            },
        ),
    ]
