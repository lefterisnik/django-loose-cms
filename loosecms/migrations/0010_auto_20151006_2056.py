# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0009_loosecmstag_loosecmstagged'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='style',
            name='plugin',
        ),
        migrations.RemoveField(
            model_name='style',
            name='styleclasses',
        ),
        migrations.RemoveField(
            model_name='styleclassinherit',
            name='styleclass',
        ),
        migrations.DeleteModel(
            name='Style',
        ),
        migrations.DeleteModel(
            name='StyleClass',
        ),
        migrations.DeleteModel(
            name='StyleClassInherit',
        ),
    ]
