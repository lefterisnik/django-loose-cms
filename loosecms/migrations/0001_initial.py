# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HtmlPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Give a symbolic name. The actual name of url provided from the field slug.', unique=True, max_length=50, verbose_name='title')),
                ('slug', models.SlugField(null=True, blank=True, help_text='The url of this page.', unique=True, verbose_name='slug')),
                ('home', models.BooleanField(default=False, help_text='Check this box if you want this page to be the home page.', verbose_name='home page')),
                ('is_template', models.BooleanField(default=False, help_text='Check this box if this is template page.', verbose_name='is template')),
                ('is_error', models.BooleanField(default=False, help_text='Check this box if this is error page.', verbose_name='is error')),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('utime', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=True, verbose_name='publish')),
                ('template', models.ForeignKey(blank=True, to='loosecms.HtmlPage', help_text='Select the template you want to render this pages.', null=True, verbose_name='template')),
            ],
            options={
                'verbose_name': 'html page',
                'verbose_name_plural': 'html pages',
            },
        ),
        migrations.CreateModel(
            name='Plugin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50, blank=True)),
                ('published', models.BooleanField(default=True, verbose_name='publish')),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=50)),
                ('html_tag', models.CharField(max_length=50)),
                ('html_id', models.CharField(unique=True, max_length=50, blank=True)),
                ('css', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('element_is_grid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='StyleClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField(null=True, blank=True)),
                ('from_source', models.BooleanField(default=False)),
                ('override', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'classes',
                'verbose_name_plural': 'classes',
            },
        ),
        migrations.CreateModel(
            name='StyleClassInherit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('css', models.TextField()),
                ('styleclass', models.ForeignKey(to='loosecms.StyleClass')),
            ],
            options={
                'verbose_name': 'classes inheritance',
                'verbose_name_plural': 'classes inheritance',
            },
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('plugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loosecms.Plugin')),
                ('title', models.CharField(help_text='Give the name of the column.', max_length=200, verbose_name='title')),
                ('slug', models.SlugField(help_text='Give the slug of the column to be used as id in html.', unique=True, verbose_name='slug')),
                ('width', models.IntegerField(help_text='Give the width of the column.', verbose_name='width')),
                ('order', models.IntegerField(default=0, verbose_name='order')),
            ],
            options={
                'verbose_name': 'column',
                'verbose_name_plural': 'columns',
            },
            bases=('loosecms.plugin',),
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('plugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='loosecms.Plugin')),
                ('title', models.CharField(help_text='Give the name of the row.', max_length=200, verbose_name='title')),
                ('slug', models.SlugField(help_text='Give the slug of the row to be used as id in html.', unique=True, verbose_name='slug')),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('page', models.ForeignKey(verbose_name='page', to='loosecms.HtmlPage', help_text='Select the page or the template to add this row.')),
            ],
            options={
                'verbose_name': 'row',
                'verbose_name_plural': 'rows',
            },
            bases=('loosecms.plugin',),
        ),
        migrations.AddField(
            model_name='style',
            name='plugin',
            field=models.ForeignKey(to='loosecms.Plugin'),
        ),
        migrations.AddField(
            model_name='style',
            name='styleclasses',
            field=models.ManyToManyField(to='loosecms.StyleClass'),
        ),
        migrations.AddField(
            model_name='plugin',
            name='placeholder',
            field=models.ForeignKey(blank=True, to='loosecms.Plugin', null=True),
        ),
    ]
