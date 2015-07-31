# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django import forms
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
        }

    #def __init__(self, *args, **kwargs):
    #    super(StyleForm, self).__init__(*args, **kwargs)
    #    self.fields['styleclasses'].widget = RelatedFieldWidgetWrapper(FilteredSelectMultiple('Classes', False),
    #                                                             Style._meta.get_field('styleclasses').rel,
    #                                                              self.admin_site)


class MovePluginForm(forms.Form):
    new_page = forms.ModelChoiceField(queryset=HtmlPage.objects.all(),
                                      label=_('New page'),
                                      required=True,
                                      help_text=_('Give the new page to move the plugin.'))
    new_placeholder = forms.ModelChoiceField(queryset=ColumnManager.objects.all(),
                                             label=_('New placeholder'),
                                             required=True,
                                             help_text=_('Give the new placeholder column of the page you select above.'))

    def __init__(self, *args, **kwargs):
        page = kwargs.pop('page', None)
        plugin = kwargs.pop('plugin', None)
        super(MovePluginForm, self).__init__(*args, **kwargs)

        if page:
            self.fields['new_page'].queryset = HtmlPage.objects.filter(~Q(pk=page))
        if plugin:
            self.fields['new_placeholder'].queryset = ColumnManager.objects.filter(~Q(placeholder=plugin))

class RowManagerForm(PluginForm):
    class Meta(PluginForm.Meta):
        model = RowManager


class ColumnManagerForm(PluginForm):
    class Meta(PluginForm.Meta):
        model = ColumnManager