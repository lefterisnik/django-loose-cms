# -*- coding: utf-8 -*-
from django.forms import widgets
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class UploadFilePathWidget(widgets.Select):

    class Media:
        js = ('loosecms/loosecms/js/admin/filemanager.js', )

    def __init__(self, attrs=None, upload_to=()):
        super(UploadFilePathWidget, self).__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.upload_to = upload_to

    def render(self, name, value, attrs=None, choices=()):
        print self.choices
        filemanager_url = reverse('admin:admin_filemanager', )
        filemanager_url += '?to_field=%s&upload_to=%s' % (attrs['id'], self.upload_to)
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        input_group_start = '<div class="input-group">'
        input_group_finish = '</div>'
        output = [input_group_start, format_html('<select{}>', flatatt(final_attrs))]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</select>')
        span = '<span class="input-group-btn">\
                <a href="%s" data-id="%s" class="filemanager btn btn-default">Search or upload a file</a>\
                </span>' % (filemanager_url, attrs['id'])
        output.append(span)
        output.append(input_group_finish)
        return mark_safe('\n'.join(output))