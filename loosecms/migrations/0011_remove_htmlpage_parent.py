# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0010_auto_20151006_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='htmlpage',
            name='parent',
        ),
    ]
