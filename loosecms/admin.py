# -*- coding: utf-8 -*-
import os
import re
import fnmatch

from urlparse import urlparse
from bs4 import BeautifulSoup


from django.conf import settings
from django.core import urlresolvers
from django.template import RequestContext
from django.contrib import admin, messages
from django.conf.urls import patterns, url
from django.utils.encoding import force_text
from django.contrib.staticfiles import finders
from django.forms.formsets import formset_factory
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.cache import never_cache
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string, get_template

from .models import *
from .forms import *
from .plugin_pool import plugin_pool
from .utils import *
from .plugin import *


class FileManagerAdminSite(admin.AdminSite):

    def get_urls(self):
        """
        Add custom urls to filemanager admin site.
        :return: urls
        """
        urlpatterns = patterns('',
            url(r'^filemanager/$', self.admin_view(self.filemanager), name='admin_filemanager'),
        )
        return urlpatterns

    @never_cache
    def filemanager(self, request):
        """
        List files of specific path and give the upload input
        :return: path of selected file or uploaded file
        """
        errors = {}
        context = dict(
            # Include common variables for rendering the admin template.
            self.each_context(request),
            current_app=self.name,
            title=_('Select or Upload File'),
            is_popup=True,
            errors=errors,
        )

        if request.method == 'GET':
            if 'upload_to' in request.GET:
                upload_to = request.GET['upload_to']
                context.update(
                    upload_to=upload_to,
                )

        if request.method == 'POST':
            upload_to = request.POST['upload_to']
            context.update(
                    upload_to=upload_to,
                )
            if not request.FILES:
                msg = _('This field is required.')
                errors['id_document'] = msg
                context.update(
                    errors=errors
                )
            else:
                file_ = request.FILES['document']
                filename = '%s/%s' %(upload_to, file_.name)

                name = default_storage.save(filename, file_)
                context.update(
                    docs=(
                        [name.split('/')[1], '/', default_storage.path(name)],
                    )
                )
        return render(request, 'admin/filemanager_form.html', context)

site = FileManagerAdminSite('filemanager')


class HtmlPageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('is_template', 'published', 'is_error', 'home')
    list_display = ('title', 'is_template', 'home', 'published')
    list_editable = ('published', )
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'template', 'published')
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
            url(r'^(?P<page_pk>\d+)/edit_page/$', self.admin_site.admin_view(self.edit_page),
                name='admin_edit_page'),
            url(r'^(?P<page_pk>\d+)/move_plugin/(?P<pk>\d+)/api/$', self.admin_site.admin_view(self.move_plugin_api),
                name='admin_move_plugin_api'),
        )
        return my_urls + urls

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
        """
        View for the editor of a HTML page
        :param request:
        :param page_pk:
        :return: HTML
        """
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
        """
        View for adding a plugin
        :param request:
        :param page_pk:
        :return: HTML (add_view) or a script that close popup window
        """
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
        :return: HTML (change_view) or a script that close popup window
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
        """
        Prompt delete form for requested plugin
        :param request:
        :param page_pk:
        :param pk:
        :return: HTML (delete_view) or a script that close popup window
        """
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
        """
        Prompt custom move form for requested plugin
        :param request:
        :param page_pk:
        :param pk:
        :return: HTML (move_form) or a script that close popup window
        """
        plugin = get_object_or_404(Plugin, pk=pk)
        page = get_object_or_404(HtmlPage, pk=page_pk)

        if request.method == 'POST':
            form = MovePluginForm(request.POST, plugin=plugin)
            if form.is_valid():
                new_placeholder = form.cleaned_data['new_placeholder']
                new_page = form.cleaned_data['new_page']

                if new_page and plugin.type == 'RowPlugin':
                    rowmanager = plugin.rowmanager
                    rowmanager.page = new_page
                    if new_placeholder:
                        rowmanager.placeholder = new_placeholder
                    else:
                        rowmanager.placeholder = None
                    rowmanager.save()
                elif new_placeholder and plugin.type == 'ColumnPlugin':
                    plugin.placeholder = new_placeholder
                    plugin.save()

                return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')
        else:
            form = MovePluginForm(plugin=plugin)

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            current_app=self.admin_site.name,
            form=form,
            is_popup=True,
            title=_('Move plugin'),
            form_url=urlresolvers.reverse('admin:admin_move_plugin', args=(page_pk, pk))
        )
        return render(request, 'admin/move_form.html', context)

    def edit_style(self, request, page_pk, pk):
        """
        Prompt edit style form for requested plugin
        :param request:
        :param page_pk:
        :param pk:
        :return: HTML (edit_style_form) or a script that close popup window
        """
        page = get_object_or_404(HtmlPage, pk=page_pk)

        plugin = get_object_or_404(Plugin.objects, pk=pk)

        # Create the modeladmin instance of the plugin
        plugin_modeladmin_cls = plugin_pool.plugins[plugin.type]
        plugin_model = plugin_modeladmin_cls.model
        plugin_modeladmin = plugin_modeladmin_cls(plugin_model, self.admin_site)

        # Fetch the plugin manager that contain the appropriate context variables
        plugin_manager = get_object_or_404(plugin_model, pk=pk)

        if plugin_modeladmin.__class__.__name__ == 'RowPlugin':
            rendered_template = '<div class="row" id="'+ plugin_manager.slug +'">'
        elif plugin_modeladmin.__class__.__name__ == 'ColumnPlugin':
            rendered_template = '<div class="col-lg-' + plugin_manager.width + '" id="' + plugin_manager.slug + '">'
        else:
            if plugin_modeladmin.template:
                request_context = RequestContext(request)
                rendered_template = plugin_modeladmin.render_to_string(request_context, plugin_manager)

        # Normalize template without whitespaces
        lines = rendered_template.split('\n')
        rendered_template = '\n'.join([line for line in lines if not re.match(r'^\s*$', line)])

        if request.method == 'GET':
            # Find all html tags from them template
            parser = MyHtmlParser()
            parser.feed(rendered_template)


            # Find all css of the project and pass it to the css list
            csss = []
            for finder in finders.get_finders():
                for file_ in list(finder.list(['*.js', '*.min.css', '*.woff2', '*.svg', '*.eot', '*.woff', '*.ttf',
                                              '*.png', '*.jpg', '*.otf', '*.psd', '*.map', '*.txt', '*.gif', '*.md'])):
                    csss.append(finders.find(file_[0]))

            populate_cssclasses_attrs(csss, parser.plugin_style)

            StyleFormSet = formset_factory(StyleForm, formset=BaseStyleFormSet, extra=0, can_delete=True)
            formset = StyleFormSet(initial=get_initial_values(parser.plugin_style), admin_site=self.admin_site)

            context = dict(
                # Include common variables for rendering the admin template.
                self.admin_site.each_context(request),
                current_app=self.admin_site.name,
                title=_('Edit stylesheet'),
                formset=formset,
                is_popup=True,
                template=rendered_template,
                form_url=urlresolvers.reverse('admin:admin_edit_style', args=(page_pk, pk))
            )
            return render(request, 'admin/edit_style_form.html', context)

        if request.method == 'POST':
            StyleFormSet = formset_factory(StyleForm, formset=BaseStyleFormSet)
            formset = StyleFormSet(data=request.POST, files=request.FILES, admin_site=self.admin_site)
            if formset.is_valid():
                for form in formset:
                    styleclasses = form.cleaned_data['styleclasses']
                    css = form.cleaned_data['css']
                    original_html = form.cleaned_data['original_html']

                    add_styleclasses = False

                    html = BeautifulSoup(original_html, 'html.parser')
                    if html.contents[0].get('class'):
                        original_styleclasses = html.contents[0]['class']
                        original_styleclasses.sort()
                        styleclasses = [x.title for x in styleclasses]
                        styleclasses.sort()
                        if styleclasses != original_styleclasses:
                            add_styleclasses = True
                    else:
                        if styleclasses:
                            add_styleclasses = True

                    if add_styleclasses or css:
                        #TODO: copy template to a new template folder (template app folder for
                        #overriding them) and change the classes
                        pass
                return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')
            else:
                context = dict(
                    # Include common variables for rendering the admin template.
                    self.admin_site.each_context(request),
                    current_app=self.admin_site.name,
                    title=_('Edit stylesheet'),
                    formset=formset,
                    is_popup=True,
                    template=rendered_template,
                    form_url=urlresolvers.reverse('admin:admin_edit_style', args=(page_pk, pk))
                )
                return render(request, 'admin/edit_style_form.html', context)

    def move_plugin_api(self, request, page_pk, pk):
        """
        Api that refresh select boxes of move form
        :param request:
        :param page_pk:
        :param pk:
        :return: JSON array of the new placeholders
        """
        if request.method == 'GET':
            plugin = get_object_or_404(Plugin, pk=pk)

            if plugin.type == 'RowPlugin':
                if 'selected_page' in request.GET:
                    selected_page = request.GET['selected_page']
                    if selected_page:
                        page = get_object_or_404(HtmlPage, pk=selected_page)

                        rows = RowManager.objects.filter(placeholder__isnull=False)\
                            .values_list('placeholder', flat=True)
                        plugins = Plugin.objects.filter(placeholder__isnull=False)\
                            .values_list('placeholder', flat=True)
                        columns = ColumnManager.objects.filter((Q(pk__in=rows) | ~Q(pk__in=plugins))
                                                               & ~Q(placeholder=plugin) & ~Q(pk=plugin.placeholder)
                                                               & Q(placeholder__rowmanager__page=page))\
                            .values('type', 'title', 'pk')
                    else:
                        rows = RowManager.objects.filter(placeholder__isnull=False)\
                            .values_list('placeholder', flat=True)
                        plugins = Plugin.objects.filter(placeholder__isnull=False)\
                            .values_list('placeholder', flat=True)
                        columns = ColumnManager.objects.filter((Q(pk__in=rows) | ~Q(pk__in=plugins))
                                                               & ~Q(placeholder=plugin) & ~Q(pk=plugin.placeholder))\
                            .values('type', 'title', 'pk')

                return JsonResponse(list(columns), safe=False)
            elif plugin.type == 'ColumnPlugin':
                if 'selected_page' in request.GET:
                    selected_page = request.GET['selected_page']
                    if selected_page:
                        page = get_object_or_404(HtmlPage, pk=selected_page)
                        rows = RowManager.objects.filter(page=page).exclude(pk=plugin.placeholder)\
                            .values('type', 'title', 'pk')
                    else:
                        rows = RowManager.objects.exclude(pk=plugin.placeholder)\
                            .values('type', 'title', 'pk')

                return JsonResponse(list(rows), safe=False)



class StyleAdmin(admin.ModelAdmin):
    filter_horizontal = ('styleclasses',)
    #form = StyleForm

    #def __init__(self, model, admin_site):
    #    self.form.admin_site = admin_site
    #    super(StyleAdmin, self).__init__(model, admin_site)


class StyleClassInheritInline(admin.StackedInline):
    model = StyleClassInherit
    extra = 1


class StyleClassAdmin(admin.ModelAdmin):
    inlines = [
        StyleClassInheritInline
    ]

admin.site.register(HtmlPage, HtmlPageAdmin)
admin.site.register(Style, StyleAdmin)
admin.site.register(StyleClassInherit)
admin.site.register(StyleClass, StyleClassAdmin)
admin.site.register(RowManager, RowPlugin)
admin.site.register(ColumnManager, ColumnPlugin)