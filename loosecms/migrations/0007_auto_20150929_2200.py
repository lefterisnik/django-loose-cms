# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0006_auto_20150929_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='htmlpage',
            name='slug',
            field=models.CharField(null=True, max_length=150, blank=True, help_text='The url of this page.', unique=True, verbose_name='slug'),
        ),
    ]
