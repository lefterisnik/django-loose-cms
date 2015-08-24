# -*- coding:utf-8 -*-
from django import forms
from django.db.models import Q, F, Count
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


class StyleForm(forms.ModelForm):
    position = forms.CharField(widget=forms.HiddenInput(), max_length=50, required=False)

    class Meta:
        model = Style
        fields = '__all__'
        widgets = {
            'plugin': forms.HiddenInput(),
            'html_tag': forms.TextInput(attrs={'class': 'vTextField form-control', 'readonly': True}),
            'css': forms.Textarea(attrs={'class': 'vLargeTextField form-control'}),
            'description': forms.Textarea(attrs={'class': 'vLargeTextField form-control'}),
            'title': forms.TextInput(attrs={'class': 'vTextField form-control'}),
            'styleid': forms.TextInput(attrs={'class': 'vTextField form-control', 'readonly': True}),
            'styleclasses': FilteredSelectMultiple('StyleClass', False),
        }

    #def __init__(self, *args, **kwargs):
    #    super(StyleForm, self).__init__(*args, **kwargs)
    #    self.fields['styleclasses'].widget = RelatedFieldWidgetWrapper(FilteredSelectMultiple('Classes', False),
    #                                                             Style._meta.get_field('styleclasses').rel,
    #                                                              self.admin_site)


class MovePluginForm(forms.Form):
    required_css_class = 'required'
    new_page = forms.ModelChoiceField(queryset=HtmlPage.objects.all(),
                                      label=_('New page'),
                                      required=False,
                                      help_text=_('Give the new page to move the plugin.'))
    new_placeholder = forms.ModelChoiceField(queryset=ColumnManager.objects.all(),
                                             label=_('New placeholder'),
                                             required=False,
                                             help_text=_('Give the new placeholder column of the page you select'
                                                         ' above.'))

    def __init__(self, *args, **kwargs):
        plugin = kwargs.pop('plugin', None)
        super(MovePluginForm, self).__init__(*args, **kwargs)

        if plugin:
            if plugin.type == 'RowPlugin':
                self.fields['new_page'].widget = forms.HiddenInput()
            else:
                self.fields['new_page'].queryset = HtmlPage.objects.all()

            # Fetch all columnns that have not childs (for each column, id column is not appear in placeholder_id)
            # and if have must be rowplugin
            # TODO: exam if placeholder is nested column and throw an error
            rows = RowManager.objects.filter(placeholder__isnull=False).values_list('placeholder', flat=True)
            plugins = Plugin.objects.filter(placeholder__isnull=False).values_list('placeholder', flat=True)
            columns = ColumnManager.objects.filter((Q(pk__in=rows) | ~Q(pk__in=plugins)) & ~Q(placeholder=plugin)
                                                   & ~Q(pk=plugin.placeholder))

            self.fields['new_placeholder'].queryset = columns

class RowManagerForm(PluginForm):
    class Meta(PluginForm.Meta):
        model = RowManager


class ColumnManagerForm(PluginForm):
    class Meta(PluginForm.Meta):
        model = ColumnManager
