# -*- coding: utf-8 -*-
import os
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.db.models import signals
from django.conf import settings
from django.shortcuts import render
from django.utils.importlib import import_module
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError


def update_css_file(sender, instance, created, **kwargs):
    styleclasses = StyleClass.objects.filter(from_source=False)
    f = open(os.path.join(settings.BASE_DIR, 'static/tsschgr/css/cms-style.css'), 'w')

    for styleclass in styleclasses:
        f.write('.%s {\n' % styleclass.name)
        f.write(styleclass.css)
        f.write('}\n')

    f.close()


class Plugin(models.Model):
    type = models.CharField(max_length=50, null=True)

    placeholder = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.pk


class StyleClass(models.Model):
    title = models.CharField(max_length=50, unique=True)
    name = models.SlugField(unique=True)
    css = models.TextField()
    description = models.TextField(blank=True, null=True)
    from_source = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('classes')
        verbose_name_plural = _('classes')

signals.post_save.connect(update_css_file, sender=StyleClass)


class Style(models.Model):
    title = models.CharField(max_length=50, unique=True)
    plugin = models.ForeignKey(Plugin)
    html_tag = models.CharField(max_length=50)
    styleclasses = models.ManyToManyField(StyleClass)
    styleid = models.CharField(max_length=50, unique=True, blank=True, null=True)
    css = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title


class Page(models.Model):
    RETURN_TYPE = (
        ('0', 'HTML'),
        ('1', 'RSS'),
    )

    title = models.CharField(_('title'), max_length=50, unique=True,
            help_text=_('Give a symbolic name. The actual name of url provided from the field slug.'))
    slug = models.SlugField(_('slug'), unique=True, null=True, blank=True,
            help_text=_('The url of this page.'))

    published = models.BooleanField(_('publish'), default=True)

    type = models.CharField(_('type'), max_length='1', choices=RETURN_TYPE,
            help_text=_('Select the type you want to return this page.'))

    def get_absolute_url(self):
        if self.slug:
            return reverse('pages-info', kwargs={"page_slug": self.slug})
        else:
            return reverse('pages-home')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('pages')
        verbose_name_plural = _('pages')


class HtmlPage(Page):
    home = models.BooleanField(_('home page'), default=False,
            help_text=_('Check this box if you want this page to be the home page.'))
    template = models.ForeignKey('self', verbose_name=_('template'), blank=True, null=True,
            limit_choices_to={'is_template': True},
            help_text=_('Select the template you want to render this pages.'))
    is_template = models.BooleanField(_('is template'), default=False,
            help_text=_('Check this box if this is template page.'))
    is_error = models.BooleanField(_('is error'), default=False,
            help_text=_('Check this box if this is error page.'))
    ctime = models.DateTimeField(auto_now_add=True)

    utime = models.DateTimeField(auto_now=True)

    def render(self, request, context):
        if request.user.is_authenticated() and request.user.is_staff:
            template = 'template_staff.html'
        else:
            template = 'template.html'
        response = render(request, template, context)
        return response

    def clean(self):
        """
        Don't allow null slug and home flag False. If null slug the home flag must be True.
        :return: cleaned_data and errors
        """
        if not self.slug and not self.home:
            msg = _('With null slug must check the home flag.')
            raise ValidationError({'home': msg})

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('html pages')
        verbose_name_plural = _('html pages')


class SyndicationPage(Page):
    choices = tuple((app, app) for app in settings.INSTALLED_APPS if os.path.exists(os.path.join(settings.BASE_DIR, app, 'rss.py')))

    app = models.CharField(max_length=50, choices=choices)

    ctime = models.DateTimeField(auto_now_add=True)

    utime = models.DateTimeField(auto_now=True)

    def render(self, context):
        modname = 'rss'
        module_name = '%s.%s' % (self.app, modname)
        try:
            module = import_module(module_name)
            return module.NewsFeed().__call__(context['request'])
        except:
            return

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('syndication pages')
        verbose_name_plural = _('syndication pages')


class RowManager(Plugin):
    title = models.CharField(_('title'), max_length=200,
            help_text=_('Give the name of the row.'))
    slug = models.SlugField(_('slug'), unique=True,
            help_text=_('Give the slug of the row to be used as id in html.'))
    page = models.ForeignKey(HtmlPage, verbose_name=_('page'),
            help_text=_('Select the page or the template to add this row.'))
    order = models.IntegerField(_('order'), default=0)

    published = models.BooleanField(_('published'), default=True)

    def __unicode__(self):
        return "%s (%s)" %(self.title, self.type)

    class Meta:
        verbose_name = _('row managers')
        verbose_name_plural = _('row managers')

    def clean(self):
        """
        Don't allow same level row have the same order
        :return: cleaned_data and errors
        """
        rows = RowManager.objects.filter(placeholder=self.placeholder, page=self.page)

        for row in rows:
            if self.order == row.order and self.pk != row.pk:
                msg = _('In this place a plugin is already exist. Please change the order.')
                raise ValidationError({'order': msg})


class ColumnManager(Plugin):
    title = models.CharField(_('title'), max_length=200,
                             help_text=_('Give the name of the column.'))
    slug = models.SlugField(_('slug'), unique=True,
                            help_text=_('Give the slug of the column to be used as id in html.'))
    width = models.IntegerField(_('width'),
                                help_text=_('Give the width of the column.'))
    order = models.IntegerField(_('order'), default=0)

    published = models.BooleanField(_('published'), default=True)

    def __unicode__(self):
        return "%s (%s)" %(self.title, self.type)

    class Meta:
        verbose_name = _('column managers')
        verbose_name_plural = _('column managers')

    def clean(self):
        """
        Don't allow width to be greater than 12
        :return: cleaned_data and errors
        """
        columns = ColumnManager.objects.filter(placeholder=self.placeholder)
        sum_width = 0
        for column in columns:
            if self.pk != column.pk:
                sum_width += column.width
                if self.order == column.order:
                    msg = _('In this place a plugin is already exist. Please change the order.')
                    raise ValidationError({'order': msg})

        if sum_width + self.width > 12:
            msg = _('Width value is too big. The valid maximum value is %s.') % (12-sum_width)
            raise ValidationError({'width': msg})