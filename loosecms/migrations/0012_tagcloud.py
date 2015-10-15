# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0011_remove_htmlpage_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagCloud',
            fields=[
                ('plugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loosecms.Plugin')),
                ('title', models.CharField(help_text='Give the name of the tag cloud.', max_length=200, verbose_name='title')),
                ('slug', models.SlugField(help_text='Give the slug of the tag cloud.', unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'tag cloud',
                'verbose_name_plural': 'tag clouds',
            },
            bases=('loosecms.plugin',),
        ),
    ]
