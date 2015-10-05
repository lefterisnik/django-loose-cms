# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import loosecms.fields


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0007_auto_20150929_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='author',
            field=models.CharField(max_length=100, verbose_name='author', blank=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='description',
            field=models.CharField(max_length=200, verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='keywords',
            field=models.CharField(max_length=200, verbose_name='keywords', blank=True),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='favicon',
            field=loosecms.fields.UploadFilePathField(recursive=True, upload_to=b'images', blank=True, path=b'images', verbose_name='favicon'),
        ),
    ]
