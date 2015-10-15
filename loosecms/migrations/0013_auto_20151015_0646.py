# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0012_tagcloud'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopularTagCloud',
            fields=[
                ('plugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loosecms.Plugin')),
                ('title', models.CharField(help_text='Give the name of the tag cloud.', max_length=200, verbose_name='title')),
                ('slug', models.SlugField(help_text='Give the slug of the tag cloud.', unique=True, verbose_name='slug')),
                ('page', models.ForeignKey(verbose_name='page', to='loosecms.HtmlPage', help_text='Give the page to show the objects that tagged with this tag. Must contain a Tag plugin.')),
            ],
            options={
                'verbose_name': 'popular tag cloud',
                'verbose_name_plural': 'popular tag clouds',
            },
            bases=('loosecms.plugin',),
        ),
        migrations.RenameModel(
            old_name='TagCloud',
            new_name='Tag',
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={},
        ),
    ]
