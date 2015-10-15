# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0013_auto_20151015_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='number',
            field=models.PositiveIntegerField(default=5, help_text='Give the number of results per page', verbose_name='number', blank=True),
        ),
    ]
