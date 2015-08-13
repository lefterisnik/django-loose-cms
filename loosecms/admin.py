# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import fnmatch
import os
import tinycss
from urlparse import urlparse

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.template.loader import render_to_string
from django.conf.urls import patterns, url
from django.forms.models import modelformset_factory
from django.contrib import messages
from django.contrib import admin
from django.core import urlresolvers
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, render

from .models import *
from .forms import *
from .plugin_pool import plugin_pool
from .utils import *
from .plugin import *
import pprint
import collections


class MyHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tags = {}
        self.examed_tags  = {}

    def handle_starttag(self, tag, attrs):
        position = '%s' % ':'.join(str(i) for i in self.getpos())
        self.examed_tags[position] = []

        for pos in self.examed_tags:
            if [tag, attrs] in self.examed_tags[pos]:
                self.tags[pos + ',' + position] = self.tags.pop(pos)
                return

        self.examed_tags[position].append([tag, attrs])
        #print self.examed_tags.values()

        has_attr = False
        if len(attrs):
            position = '%s' % ':'.join(str(i) for i in self.getpos())

            if position not in self.tags:
                self.tags[position] = {}
            if tag not in self.tags[position]:
                self.tags[position][tag] = {}

            # Add values to dict
            for attr in attrs:
                if 'class' in attr or 'id' in attr:
                    if attr in self.tags[position][tag]:
                        self.tags[position][tag][attr[0]] += dict([(i, dict()) for i in attr[1].split()])
                    else:
                        self.tags[position][tag][attr[0]] = dict([(i, dict()) for i in attr[1].split()])
                    has_attr = True
                if 'style' in attr:
                    self.tags[position][tag][attr[0]] = attr[1]

            if not has_attr:
                self.tags.pop(position)
                return


class HtmlPageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('is_template', )
    list_display = ('title', 'is_template', 'type', 'published')
    list_editable = ('published', )
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'type', 'template', 'published')
        }),
        ('Advanced options',{
            'fields': ('home', 'is_template', 'is_error')
        }),
    )
    search_fields = ['title', 'slug']

    def response_add(self, request, obj, post_url_continue=None):
        """
        Return message and redirect to the appropiate edit page
        :param request:
        :param obj:
        :param post_url_continue:
        :return: HttpResponse that redirect to added page
        """
        if '_to_field' not in request.POST and '_popup' in request.POST:

            opts = self.model._meta

            msg_dict = {'name': force_text(opts.verbose_name), 'obj': force_text(obj)}
            msg = _('The %(name)s "%(obj)s" was added successfully.') % msg_dict
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponse('<script>window.parent.location.replace("'
                                + urlresolvers.reverse('admin:admin_edit_page', args=(obj.pk,))
                                + '");self.close();</script>')

        return super(HtmlPageAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        """
        Return message and redirect to the appropiate page
        :param request:
        :param obj:
        :return: HttpResponse that redirect to changed page
        """
        if '_to_field' not in request.POST and '_popup' in request.POST:

            opts = self.model._meta

            msg_dict = {'name': force_text(opts.verbose_name), 'obj': force_text(obj)}
            msg = _('The %(name)s "%(obj)s" was changed successfully.') % msg_dict
            self.message_user(request, msg, messages.SUCCESS)
            return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')

        return super(HtmlPageAdmin, self).response_add(request, obj)

    def get_urls(self):
        """
        Add custom urls to page admin.
        :return: urls
        """
        urls = super(HtmlPageAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(?P<page_pk>\d+)/add_plugin/$', self.admin_site.admin_view(self.add_plugin),
                name='admin_add_plugin'),
            url(r'^(?P<page_pk>\d+)/edit_plugin/(?P<pk>\d+)/$', self.admin_site.admin_view(self.edit_plugin),
                name='admin_edit_plugin'),
            url(r'^(?P<page_pk>\d+)/delete_plugin/(?P<pk>\d+)/$', self.admin_site.admin_view(self.delete_plugin),
                name='admin_delete_plugin'),
            url(r'^(?P<page_pk>\d+)/move_plugin/(?P<pk>\d+)/$', self.admin_site.admin_view(self.move_plugin),
                name='admin_move_plugin'),
            url(r'^(?P<page_pk>\d+)/edit_plugin/(?P<pk>\d+)/edit_style/$', self.admin_site.admin_view(self.edit_style),
                name='admin_edit_style'),
            url(r'^(?P<page_pk>\d+)/edit_page/$', self.admin_site.admin_view(self.edit_page), name='admin_edit_page'),
        )
        return my_urls + urls

    def edit_style(self, request, page_pk, pk):
        page = HtmlPage.objects.get(pk=page_pk)
        if request.method == 'GET':
            plugin_pool.discover_plugins()
            plugin = get_object_or_404(Plugin.objects, pk=pk)
            plugin_admin = plugin_pool.plugins[plugin.type](plugin_pool.plugins[plugin.type].model, self.admin_site)
            instance = plugin_admin.model.objects.get(pk=pk)

            if plugin.type == 'RowPlugin':
                template = '<div class="row" id="'+ instance.slug +'">'
            elif plugin.type == 'ColumnPlugin':
                template = '<div class="col-lg-' + instance.width + '" id="' + instance.slug + '">'
            else:
                if plugin_admin.template:
                    # TODO: give the appropiate context to return real template
                    template = render_to_string(plugin_admin.template)

            # Find all html tags from them template
            parser = MyHtmlParser()
            parser.feed(template)


            # Find all css of the project and pass it to the css list
            css = []
            for root, dirnames, filenames in os.walk(os.path.join(settings.BASE_DIR, 'static')):
                for filename in fnmatch.filter(filenames, '*.css'):
                    if 'min' not in filename:
                        css.append(os.path.join(root, filename))


            # For each css, parse it with tinycss and exam if id or class exist in them
            # and then take the attrs or declarations according to tinycss
            for css in css:
                css_parser = tinycss.make_parser('page3')
                stylesheet = css_parser.parse_stylesheet_file(css)
                for position in parser.tags:
                    for tag in parser.tags[position]:
                        for choice in parser.tags[position][tag]:
                            if choice == 'class':
                                for tag_class in parser.tags[position][tag][choice]:
                                    for rule in stylesheet.rules:
                                        if not rule.at_keyword:
                                            if rule.selector.as_css().endswith(".%s" % tag_class):
                                                parser.tags[position][tag][choice][tag_class][rule.selector.as_css()] = list(rule.declarations)
                            elif choice == 'id':
                                for tag_id in parser.tags[position][tag][choice]:
                                    for rule in stylesheet.rules:
                                        if not rule.at_keyword:
                                            if rule.selector.as_css().endswith("#" + tag_id):
                                                parser.tags[position][tag][choice][tag_id][rule.selector.as_css()] = list(rule.declarations)

            pprint.pprint(parser.tags)
            parser.tags = collections.OrderedDict(sorted(parser.tags.items()))

            def get_style(position, tag):
                if 'style' in parser.tags[position][tag]:
                    style = parser.tags[position][tag]['style']
                else:
                    style = ''

                # Get current styles and concat them with the template
                try:
                    styles = Style.objects.get(plugin=pk, html_tag=tag)
                    style += styles.css
                    return style
                except Style.DoesNotExist:
                    return style

            def get_id(position, tag):
                if 'id' in parser.tags[position][tag]:
                    for key, value in parser.tags[position][tag]['id'].items():
                        return key

                try:
                    styles = Style.objects.get(plugin=pk, html_tag=tag)
                    return styles.styleid
                except Style.DoesNotExist:
                    return None

            def get_already(position, tag):
                defaults = []
                string = ''
                for choice in parser.tags[position][tag]:
                    if choice == 'class':
                        for tag_class in parser.tags[position][tag][choice]:
                            for tag_class_name_css in parser.tags[position][tag][choice][tag_class]:
                                string += '%s {\n%s\n}\n\n' % (tag_class_name_css, '\n'.join(x.name + ": " + x.value.as_css() + ";"
                                                            for x in parser.tags[position][tag][choice][tag_class][tag_class_name_css]))
                            try:
                                styleclass = StyleClass(title=tag_class, name=tag_class, css=string, from_source=True)
                                styleclass.save()
                            except:
                                styleclass = StyleClass.objects.get(title=tag_class)
                            defaults.append(styleclass)

                return [x.pk for x in defaults]


            def get_title(position, tag):
                # Get current styles and concat them with the template
                try:
                    styles = Style.objects.get(plugin=pk, html_tag=tag)
                    return styles.title
                except Style.DoesNotExist:
                    return None

            def get_description(position, tag):
                # Get current styles and concat them with the template
                try:
                    styles = Style.objects.get(plugin=pk, html_tag=tag)
                    return styles.description
                except Style.DoesNotExist:
                    return None


            extra = len(parser.tags)
            StyleFormSet = modelformset_factory(Style, StyleForm, extra=extra, can_delete=True)

            formset = StyleFormSet(initial=[
                {'title': get_title(position, tag),
                 'plugin': pk,
                 'position': '@line %s %s' %(position, tag),
                 'html_tag': tag,
                 'css': get_style(position, tag),
                 'styleid': get_id(position, tag),
                 'description': get_description(position, tag),
                 'styleclasses': get_already(position, tag)} for position in parser.tags for tag in parser.tags[position]
            ])

            context = dict(
                # Include common variables for rendering the admin template.
                self.admin_site.each_context(request),
                title=_('Edit stylesheet'),
                formset=formset,
                is_popup=True,
                is_ajax=request.is_ajax(),
                template=template,
                form_url=urlresolvers.reverse('admin:admin_edit_style', args=(page_pk, pk))
            )
            return render(request, 'admin/edit_style_form.html', context)

        if request.method == 'POST':
            StyleFormSet = modelformset_factory(Style, StyleForm)

            formset = StyleFormSet(request.POST, request.FILES)
            if formset.is_valid():
                formset.save()
                return JsonResponse({'redirect_url': page.get_absolute_url()})
            else:
                context = dict(
                    # Include common variables for rendering the admin template.
                    self.admin_site.each_context(request),
                    formset=formset,
                    is_popup=True,
                    is_ajax=request.is_ajax(),
                    form_url=urlresolvers.reverse('admin:admin_edit_style', args=(page_pk, pk))
                )
                return render(request, 'admin/edit_style_form.html', context)

    def add_view(self, request, form_url='', extra_context=None):
        """
        Return the appropiate form or save the page
        :param request:
        :return:json or the html form
        """
        is_popup = False
        if request.META.get('HTTP_REFERER'):
            referrer = urlparse(request.META.get('HTTP_REFERER'))
            #TODO: be more specific. We arleady know all admin urls and all views
            # so we can exam the full func or hole urls.
            # In this case we have more referrers to exam
            if 'changelist_view' in str(urlresolvers.resolve(referrer.path).func):
                is_popup = False
            else:
                is_popup = True

        extra_context = extra_context or {}
        extra_context.update(
            is_popup=is_popup,
        )

        form_url = urlresolvers.reverse('admin:loosecms_htmlpage_add')

        return super(HtmlPageAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Return the appropiate form or sace the page
        :param request:
        :param object_id:
        :param form_url:
        :param extra_context:
        :return:
        """
        is_popup = False
        if request.META.get('HTTP_REFERER'):
            referrer = urlparse(request.META.get('HTTP_REFERER'))
            #TODO: be more specific. We arleady know all admin urls and all views
            # so we can exam the full func or hole urls.
            if 'changelist_view' in str(urlresolvers.resolve(referrer.path).func):
                is_popup = False
            else:
                is_popup = True


        extra_context = extra_context or {}
        extra_context.update(
            is_popup=is_popup,
        )

        form_url = urlresolvers.reverse('admin:loosecms_htmlpage_change', args=(object_id, ))

        return super(HtmlPageAdmin, self).change_view(request, object_id, form_url, extra_context)

    def edit_page(self, request, page_pk):
        if request.method == 'GET':
            all_pages = HtmlPage.objects.all()
            page = all_pages.get(pk=page_pk)
            template_pages = all_pages.filter(is_template=True)
            pages = all_pages.filter(is_template=False)

            context = dict(
                # Include common variables for rendering the admin template.
                self.admin_site.each_context(request),
                # Anything else you want in the context...
                page=page,
                template_pages=template_pages,
                pages=pages,
                title=_('Edit page'),
                is_popup=True,
            )
            context = update_context(context, page)
            return render(request, 'admin/editor_form.html', context)

    def add_plugin(self, request, page_pk):
        if request.method == 'GET':
            if 'type' in request.GET:
                type = request.GET['type']
            if 'placeholder' in request.GET:
                placeholder = request.GET['placeholder']
            else:
                placeholder = None

        if request.method == 'POST':
            if 'type' in request.POST:
                type = request.POST['type']
            if 'placeholder' in request.POST:
                placeholder = request.POST['placeholder']

        plugin_pool.discover_plugins()
        #TODO: avoid for loop, because we arleady have type plugin
        for plugin in plugin_pool.plugins:
            if type == plugin:
                page = HtmlPage.objects.get(pk=page_pk)
                plugin_admin = plugin_pool.plugins[plugin](plugin_pool.plugins[plugin].model, self.admin_site)
                plugin_admin.extra_initial_help = {
                    'page': page,
                    'type': type,
                    'placeholder': placeholder,
                }
                extra_context = {
                    'is_popup': True,
                }
                form_url = urlresolvers.reverse('admin:admin_add_plugin', args=(page_pk, ))
                response = plugin_admin.add_view(request, form_url=form_url, extra_context=extra_context)

                if plugin_admin.object_successfully_added:
                    return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')
                return response

    def edit_plugin(self, request, page_pk, pk):
        """
        Prompt edit form for requested plugin
        :param request:
        :param pk:
        :return: change_view if request is get or confirm.html if request is post
        """
        page = HtmlPage.objects.get(pk=page_pk)
        plugin_pool.discover_plugins()
        plugin = get_object_or_404(Plugin.objects, pk=pk)
        plugin_admin = plugin_pool.plugins[plugin.type](plugin_pool.plugins[plugin.type].model, self.admin_site)

        extra_context = {
            'is_popup': True,
        }
        form_url = urlresolvers.reverse('admin:admin_edit_plugin', args=(page_pk, pk))
        response = plugin_admin.change_view(request, pk, form_url=form_url, extra_context=extra_context)
        if plugin_admin.object_successfully_changed:
            return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')
        return response

    def delete_plugin(self, request, page_pk, pk):
        page = HtmlPage.objects.get(pk=page_pk)
        plugin_pool.discover_plugins()
        plugin = get_object_or_404(Plugin.objects, pk=pk)
        plugin_admin = plugin_pool.plugins[plugin.type](plugin_pool.plugins[plugin.type].model, self.admin_site)

        extra_context = {
            'is_popup': True,
            'delete_url': urlresolvers.reverse('admin:admin_delete_plugin', args=(page_pk, pk))
        }
        response = plugin_admin.delete_view(request, pk, extra_context=extra_context)
        if plugin_admin.object_successfully_deleted:
            return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')
        return response

    def move_plugin(self, request, page_pk, pk):
        if request.method == 'POST':
            form = MovePluginForm(request.POST)
            if form.is_valid():
                new_placeholder = form.cleaned_data['new_placeholder']
                new_page = form.cleaned_data['new_page']

                plugin_pool.discover_plugins()
                plugin = get_object_or_404(Plugin.objects, pk=pk)
                plugin_model = plugin_pool.plugins[plugin.type].model
                instance = plugin_model.objects.get(pk=pk)
                instance.placeholder = new_placeholder
                if instance.type == 'RowPlugin':
                    instance.page = new_page
                instance.save()
                return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')
        else:
            form = MovePluginForm(page=page_pk, plugin=pk)

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            form=form,
            is_popup=True,
            title=_('Move plugin'),
            form_url=urlresolvers.reverse('admin:admin_move_plugin', args=(page_pk, pk))
        )
        return render(request, 'admin/move_form.html', context)



class StyleAdmin(admin.ModelAdmin):
    filter_horizontal = ('styleclasses',)
    form = StyleForm

    def __init__(self, model, admin_site):
        self.form.admin_site = admin_site
        super(StyleAdmin, self).__init__(model, admin_site)


class StyleClassAdmin(admin.ModelAdmin):
    prepopulated_fields = {'name': ('title', )}


admin.site.register(HtmlPage, HtmlPageAdmin)
admin.site.register(SyndicationPage)
admin.site.register(Style, StyleAdmin)
admin.site.register(StyleClass, StyleClassAdmin)
admin.site.register(RowManager, RowPlugin)
admin.site.register(ColumnManager, ColumnPlugin)