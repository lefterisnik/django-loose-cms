# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0014_tag_number'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tag',
            new_name='Category',
        ),
        migrations.RenameModel(
            old_name='PopularTagCloud',
            new_name='PopularCategoryCloud',
        ),
        migrations.AlterModelOptions(
            name='popularcategorycloud',
            options={},
        ),
    ]
