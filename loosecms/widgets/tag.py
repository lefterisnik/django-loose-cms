# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from taggit.models import Tag

from taggit.forms import TagWidget


class LoosecmsTagWidget(TagWidget):

    class Media:
        css = {
            'all': (
                '//code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css',
                'loosecms/external/bootstrap-tokenfield/css/bootstrap-tokenfield.min.css',
            )
        }
        js = (
            '//ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js',
            'loosecms/external/bootstrap-tokenfield/bootstrap-tokenfield.min.js',
        )

    def render(self, name, value, attrs=None):
        tags = Tag.objects.all()
        return mark_safe(render_to_string('taggit/widget_additional.html', {'name': name, 'tags': tags})) + \
               super(LoosecmsTagWidget, self).render(name, value, attrs)


