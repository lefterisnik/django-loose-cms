# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0015_auto_20151015_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plugin',
            name='type',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
