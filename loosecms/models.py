# -*- coding: utf-8 -*-
import os
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.conf import settings
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError

from .plugin_pool import plugin_pool
from .fields import UploadFilePathField
from .signals import update_context_processor


def update_css_file(sender, instance, created, **kwargs):
    styleclasses = StyleClass.objects.filter(from_source=False)
    f = open(os.path.join(settings.BASE_DIR, 'static/loosecms/loosecms/css/cms-style.css'), 'w')

    for styleclass in styleclasses:
        for styleclassinherit in styleclass.styleclassinherit_set.all():
            f.write('%s {\n' % styleclassinherit.title)
            f.write(styleclassinherit.css)
            f.write('}\n')
    f.close()


class LooseCMSConfiguration(models.Model):

    site = models.OneToOneField(Site)

    favicon = UploadFilePathField(_('favicon'), upload_to='images', path='images')

    ckeditor_upload_path = models.CharField(_('ckeditor upload path'), max_length=100, default='images')

    def __unicode__(self):
        return self.site.name

    class Meta:
        app_label = 'sites'
        verbose_name = _('Loose CMS Configuration')
        verbose_name_plural = _('Loose CMS Configurations')


class Plugin(models.Model):
    default_type = None

    type = models.CharField(max_length=50, blank=True)

    placeholder = models.ForeignKey('self', blank=True, null=True)

    published = models.BooleanField(_('publish'), default=True)

    def save(self, *args, **kwargs):
        if self.type is None:
            self.type = self.default_type
        super(Plugin, self).save(*args, **kwargs)

    def __unicode__(self):
        plugin_modeladmin_cls = plugin_pool.plugins[self.type]
        child_plugin = getattr(self, plugin_modeladmin_cls.model._meta.model_name)
        return "%s (%s)" % (child_plugin.title, self.type)


class StyleClass(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    from_source = models.BooleanField(default=False)
    override = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('classes')
        verbose_name_plural = _('classes')


class StyleClassInherit(models.Model):
    title = models.TextField()
    css = models.TextField()
    styleclass = models.ForeignKey(StyleClass)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('classes inheritance')
        verbose_name_plural = _('classes inheritance')


class Style(models.Model):
    title = models.CharField(max_length=50, unique=True)
    plugin = models.ForeignKey(Plugin)
    html_tag = models.CharField(max_length=50)
    html_id = models.CharField(max_length=50, unique=True, blank=True)
    styleclasses = models.ManyToManyField(StyleClass)
    css = models.TextField(blank=True)
    description = models.TextField(blank=True)
    element_is_grid = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class HtmlPage(models.Model):
    title = models.CharField(_('title'), max_length=50, unique=True,
            help_text=_('Give a symbolic name. The actual name of url provided from the field slug.'))
    slug = models.SlugField(_('slug'), unique=True, null=True, blank=True,
            help_text=_('The url of this page.'))
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

    published = models.BooleanField(_('publish'), default=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        if self.slug:
            return reverse('pages-info', kwargs={"page_slug": self.slug})
        else:
            return reverse('pages-home')

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
        Don't allow two of home, is_template and is_error to be selected
        Don't allow two or more home pages published
        Don't allow two or more error pages published
        :return: cleaned_data and errors
        """
        htmlpages = HtmlPage.objects.all()

        if not self.slug and not self.home:
            msg = _('With null slug must check the home flag.')
            raise ValidationError({'home': msg})

        if (self.is_error and (self.home or self.is_template)) or \
                (self.is_template and (self.home or self.is_error)) or \
                (self.home and (self.is_error or self.is_template)):
            msg = _('Only one checkbox must be checked.')
            raise ValidationError({'home': msg, 'is_error': msg, 'is_template': msg})

        if self.home and self.published:
            for htmlpage in htmlpages:
                if htmlpage.home and htmlpage.published and self.pk != htmlpage.pk:
                    msg = _('There is already a published home page. Only one page can be the home page and published')
                    raise ValidationError({'home': msg})

        if self.is_error and self.published:
            for htmlpage in htmlpages:
                if htmlpage.is_error and htmlpage.published and self.pk != htmlpage.pk:
                    msg = _('There is already a published error page. Only one page can be the error page and published')
                    raise ValidationError({'is_error': msg})

    class Meta:
        verbose_name = _('html page')
        verbose_name_plural = _('html pages')


class Row(Plugin):
    default_type = "RowPlugin"

    title = models.CharField(_('title'), max_length=200,
            help_text=_('Give the name of the row.'))
    slug = models.SlugField(_('slug'), unique=True,
            help_text=_('Give the slug of the row to be used as id in html.'))
    page = models.ForeignKey(HtmlPage, verbose_name=_('page'),
            help_text=_('Select the page or the template to add this row.'))
    order = models.IntegerField(_('order'), default=0)

    def __unicode__(self):
        return "%s (%s)" %(self.title, self.type)

    class Meta:
        verbose_name = _('row')
        verbose_name_plural = _('rows')

    def clean(self):
        """
        Don't allow same level row have the same order
        :return: cleaned_data and errors
        """
        rows = Row.objects.filter(placeholder=self.placeholder, page=self.page)

        for row in rows:
            if self.order == row.order and self.pk != row.pk:
                msg = _('In this place a plugin is already exist. Please change the order.')
                raise ValidationError({'order': msg})


class Column(Plugin):
    default_type = "ColumnPlugin"

    title = models.CharField(_('title'), max_length=200,
                             help_text=_('Give the name of the column.'))
    slug = models.SlugField(_('slug'), unique=True,
                            help_text=_('Give the slug of the column to be used as id in html.'))
    width = models.IntegerField(_('width'),
                                help_text=_('Give the width of the column.'))
    order = models.IntegerField(_('order'), default=0)

    def __unicode__(self):
        return "%s (%s)" %(self.title, self.type)

    class Meta:
        verbose_name = _('column')
        verbose_name_plural = _('columns')

    def clean(self):
        """
        Don't allow width to be greater than 12
        :return: cleaned_data and errors
        """
        columns = Column.objects.filter(placeholder=self.placeholder)
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


post_save.connect(update_css_file, sender=StyleClassInherit)
post_save.connect(update_context_processor, sender=LooseCMSConfiguration)