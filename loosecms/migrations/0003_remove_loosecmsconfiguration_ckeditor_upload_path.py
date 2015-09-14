# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0002_loosecmsconfiguration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loosecmsconfiguration',
            name='ckeditor_upload_path',
        ),
    ]
