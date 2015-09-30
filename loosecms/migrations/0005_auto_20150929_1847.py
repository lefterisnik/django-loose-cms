# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0004_auto_20150914_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='htmlpage',
            name='parent',
            field=models.ForeignKey(related_name='child', blank=True, to='loosecms.HtmlPage', help_text='Select the parent page.', null=True, verbose_name='parent'),
        ),
        migrations.AlterField(
            model_name='htmlpage',
            name='template',
            field=models.ForeignKey(related_name='inherit', blank=True, to='loosecms.HtmlPage', help_text='Select the template you want to render this pages.', null=True, verbose_name='template'),
        ),
    ]
