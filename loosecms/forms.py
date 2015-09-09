# -*- coding:utf-8 -*-
from django import forms
from django.db.models import Q
from django.forms.formsets import BaseFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.related import ManyToManyRel
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, FilteredSelectMultiple

from .models import *

class PluginForm(forms.ModelForm):

    class Meta:
        model = Plugin
        fields = '__all__'
        widgets = {
            'type': forms.HiddenInput(),
            'placeholder': forms.HiddenInput(),
        }


class HtmlPageTemplateForm(forms.ModelForm):

    class Meta:
        model = HtmlPage
        exclude = ('template', 'home')
        widgets = {
            'type': forms.HiddenInput(),
            'is_template': forms.HiddenInput(),
        }


class HtmlPageForm(forms.ModelForm):

    class Meta:
        model = HtmlPage
        fields = '__all__'
        widgets = {
            'type': forms.HiddenInput(),
            'is_template': forms.HiddenInput(),
        }


class BaseStyleFormSet(BaseFormSet):

    def __init__(self, admin_site, *args, **kwargs):
        self.admin_site = admin_site
        super(BaseStyleFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        defaults = {
            'admin_site': self.admin_site,
        }
        defaults.update(kwargs)
        return super(BaseStyleFormSet, self)._construct_form(i, **defaults)


class StyleForm(forms.Form):
    required_css_class = 'required'
    original_html = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}),
                                    max_length=150)
    html_tag = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}),
                               max_length=150,
                               required=True)
    html_id = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}),
                              max_length=150,
                              required=False)
    css = forms.CharField(widget=forms.Textarea(),
                          required=False)
    styleclasses = forms.ModelMultipleChoiceField(queryset=StyleClass.objects.all(),
                                                  required=False)
    position = forms.CharField(widget=forms.HiddenInput(),
                               max_length=100,
                               required=False)

    def __init__(self, *args, **kwargs):
        self.admin_site = kwargs.pop('admin_site', None)
        super(StyleForm, self).__init__(*args, **kwargs)
        self.fields['styleclasses'].widget = RelatedFieldWidgetWrapper(FilteredSelectMultiple('Classes', False),
                                                                       Style._meta.get_field('styleclasses').rel,
                                                                       self.admin_site)
        self.fields['styleclasses'].queryset = StyleClass.objects.all()


class MovePluginForm(forms.Form):
    required_css_class = 'required'
    new_page = forms.ModelChoiceField(queryset=HtmlPage.objects.all(),
                                      label=_('New page'),
                                      required=False,
                                      help_text=_('Select the new page that you want the plugin to move. You can '
                                                  'select this box if you want to make it a root row plugin in '
                                                  'another page'))
    new_placeholder = forms.ModelChoiceField(queryset=Column.objects.all(),
                                             label=_('New placeholder'),
                                             required=False,
                                             help_text=_('Select the new placeholder. You can select this box if you '
                                                         'want ot move the plugin in a specific column. There is no '
                                                         'need to select the new page field because all columns knows '
                                                         'the page that are placed.'))

    def __init__(self, *args, **kwargs):
        self.plugin = kwargs.pop('plugin', None)
        super(MovePluginForm, self).__init__(*args, **kwargs)

        if self.plugin:
            if self.plugin.type == 'RowPlugin':
                # If plugin owns to a template page then show only the pages that have not this template as template
                if self.plugin.row.page.is_template:
                    pages = HtmlPage.objects.exclude(template=self.plugin.row.page.pk)\
                        .exclude(pk=self.plugin.row.page.pk)
                    if pages.count() == 0:
                        self.fields['new_page'].widget = forms.HiddenInput()
                    else:
                        self.fields['new_page'].queryset = pages
                        self.fields['new_page'].required = True
                else:
                    self.fields['new_page'].required = True

                # Fetch all columnns that have not childs (for each column, id column is not appear in placeholder_id)
                # and if have must be rowplugin
                # TODO: exam if placeholder is nested column and throw an error
                rows = Row.objects.filter(placeholder__isnull=False).values_list('placeholder', flat=True)
                plugins = Plugin.objects.filter(placeholder__isnull=False).values_list('placeholder', flat=True)
                columns = Column.objects.filter((Q(pk__in=rows) | ~Q(pk__in=plugins)) & ~Q(placeholder=self.plugin)
                                                       & ~Q(pk=self.plugin.placeholder))

                self.fields['new_placeholder'].queryset = columns
            elif self.plugin.type == 'ColumnPlugin':
                # TODO: exam if placeholder is enough space for the new column
                rows = Row.objects.exclude(pk=self.plugin.placeholder)

                self.fields['new_placeholder'].queryset = rows
                self.fields['new_placeholder'].required = True

    def clean(self):
        cleaned_data = super(MovePluginForm, self).clean()
        new_page = cleaned_data.get('new_page')
        new_placeholder = cleaned_data.get('new_placeholder')
        if self.plugin.type == 'RowPlugin':
            if new_placeholder and not new_page:
                msg = _('You have to select a page in order to list the appropriate placeholders.')
                self.add_error('new_page', msg)

            if not new_placeholder and not new_page:
                msg = _('You have to select a page or a page and a placeholder.')
                raise ValidationError(msg)
        elif self.plugin.type == 'ColumnPlugin':
            if not new_placeholder and not new_page:
                msg = _('You have to select a placeholder or a page and a placeholder.')
                raise ValidationError(msg)

            if new_page and not new_placeholder:
                msg = _('You have to select a placeholder.')
                self.add_error('new_placeholder', msg)


class SelectPluginForm(forms.Form):
    required_css_class = 'required'
    plugin = forms.ModelChoiceField(queryset=Plugin.objects.all(),
                                    label=_('Select plugin'),
                                    required=True,
                                    help_text=_('Select the plugin to attach to this placeholder.'))

    def __init__(self, *args, **kwargs):
        self.plugin = kwargs.pop('plugin', None)
        super(SelectPluginForm, self).__init__(*args, **kwargs)

        if self.plugin:
            if self.plugin.type == 'RowPlugin':
                columns = Column.objects.all()
                self.fields['plugin'].queryset = columns
            elif self.plugin.type == 'ColumnPlugin':
                plugins = Plugin.objects.exclude(type='ColumnPlugin')
                self.fields['plugin'].queryset = plugins

