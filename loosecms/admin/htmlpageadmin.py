# -*- coding: utf-8 -*-
from urlparse import urlparse

from django.conf.urls import url
from django.core import urlresolvers
from django.contrib import admin, messages
from django.utils.encoding import force_text
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, JsonResponse, Http404

from ..models import HtmlPage
from ..forms import *
from ..utils.render import update_context
from ..plugin_pool import plugin_pool


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

    def get_urls(self):
        """
        Add custom urls to page admin.
        :return: urls
        """
        urls = super(HtmlPageAdmin, self).get_urls()
        htmlpage_urls = [
            url(r'^(?P<page_pk>\d+)/edit_page/$', self.admin_site.admin_view(self.edit_page),
                name='admin_edit_page'),
            url(r'^(?P<page_pk>\d+)/add_placeholder/$', self.admin_site.admin_view(self.add_placeholder),
                name='admin_add_placeholder'),

            # Plugin urls
            url(r'^add_plugin/$', self.admin_site.admin_view(self.add_plugin),
                name='admin_add_plugin'),
            url(r'^edit_plugin/(?P<pk>\d+)/$', self.admin_site.admin_view(self.edit_plugin),
                name='admin_edit_plugin'),
            url(r'^delete_plugin/(?P<pk>\d+)/$', self.admin_site.admin_view(self.delete_plugin),
                name='admin_delete_plugin'),
            url(r'^move_plugin/(?P<pk>\d+)/$', self.admin_site.admin_view(self.move_plugin),
                name='admin_move_plugin'),
            url(r'^select_plugin/(?P<pk>\d+)/$', self.admin_site.admin_view(self.select_plugin),
                name='admin_select_plugin'),
            url(r'^remove_plugin/(?P<pk>\d+)/$', self.admin_site.admin_view(self.remove_plugin),
                name='admin_remove_plugin'),

            # API urls
            url(r'^api/move_plugin/(?P<pk>\d+)/$', self.admin_site.admin_view(self.move_plugin_api),
                name='admin_move_plugin_api'),
        ]

        # Fetch extra admin page urls from plugins
        plugin_urls = []
        for plugin, cls in plugin_pool.plugins.items():
            if cls.plugin_extra_links:
                plugin_modeladmin = cls(cls.model, self.admin_site)
                plugin_urls += plugin_modeladmin.get_urls()

        return plugin_urls + htmlpage_urls + urls

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

    def add_view(self, request, form_url='', extra_context=None):
        """
        Return the appropiate form or save the page
        :param request:
        :return:json or the html form
        """
        is_popup = False
        if '_popup' not in request.GET and '_to_field' not in request.GET:
            if request.META.get('HTTP_REFERER'):
                referrer = urlparse(request.META.get('HTTP_REFERER'))
                if 'edit_page' in str(urlresolvers.resolve(referrer.path).func) or \
                    'detail' in str(urlresolvers.resolve(referrer.path).func):
                    is_popup = True
                else:
                    is_popup = False

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
        if '_popup' not in request.GET and '_to_field' not in request.GET:
            if request.META.get('HTTP_REFERER'):
                referrer = urlparse(request.META.get('HTTP_REFERER'))
                if 'edit_page' in str(urlresolvers.resolve(referrer.path).func) or \
                    'detail' in str(urlresolvers.resolve(referrer.path).func):
                    is_popup = True
                else:
                    is_popup = False

            extra_context = extra_context or {}
            extra_context.update(
                is_popup=is_popup,
            )

            form_url = urlresolvers.reverse('admin:loosecms_htmlpage_change', args=(object_id, ))

        return super(HtmlPageAdmin, self).change_view(request, object_id, form_url, extra_context)

    @never_cache
    def edit_page(self, request, page_pk):
        """
        View for the editor of a HTML page
        :param request:
        :param page_pk:
        :return: HTML
        """
        if request.method == 'GET':
            all_pages = HtmlPage.objects.all()
            page = get_object_or_404(HtmlPage, pk=page_pk)
            template_pages = all_pages.filter(is_template=True)
            pages = all_pages.filter(is_template=False)

            context = dict(
                # Include common variables for rendering the admin template.
                self.admin_site.each_context(request),
                # Anything else you want in the context...
                page=page,
                template_pages=template_pages,
                pages=pages,
                title=_('Edit page')
            )
            context = update_context(context, page)
            return render(request, 'admin/editor_form.html', context)

    def _wrapper_add_plugin(self, request, page=None):
        #TODO: Raise 404 when type is not defined
        #TODO: Riase 404 when plugin has not placeholder. Exception rowplugin
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

        if type in plugin_pool.plugins:
            plugin_modeladmin_cls = plugin_pool.plugins[type]
            plugin_model = plugin_modeladmin_cls.model
            plugin_modeladmin = plugin_modeladmin_cls(plugin_model, self.admin_site)
            if request.method == 'GET':
                if page is None and placeholder:
                    placeholder_plugin = Plugin.objects.get(pk=placeholder)
                    if placeholder_plugin.type == 'RowPlugin':
                        page = placeholder_plugin.row.page
                    elif placeholder_plugin.placeholder.type == 'RowPlugin':
                        page = placeholder_plugin.placeholder.row.page

                plugin_modeladmin.extra_initial_help = dict(
                    page=page if page else None,
                    placeholder=placeholder,
                )

            extra_context = dict(
                is_popup = True
            )
            form_url = urlresolvers.reverse('admin:admin_add_plugin')
            response = plugin_modeladmin.add_view(request, form_url=form_url, extra_context=extra_context)

            if plugin_modeladmin.object_successfully_added and not plugin_modeladmin.plugin_cke:
                return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')
            return response

    @never_cache
    def add_placeholder(self, request, page_pk):
        """
        View for adding a row plugin as placeholder. In this view is nessecary to have the page_pk
        :param request:
        :param page_pk: HTML (add_view) or a script that close popup window
        :return:
        """
        page = get_object_or_404(HtmlPage, pk=page_pk)
        return self._wrapper_add_plugin(request, page)


    @never_cache
    def add_plugin(self, request):
        """
        View for adding a plugin. In this view the page will get it from placeholder row
        :param request:
        :return: HTML (add_view) or a script that close popup window
        """
        return self._wrapper_add_plugin(request)


    @never_cache
    def edit_plugin(self, request, pk):
        """
        Prompt edit form for requested plugin
        :param request:
        :param pk:
        :return: HTML (change_view) or a script that close popup window
        """
        plugin = get_object_or_404(Plugin.objects, pk=pk)
        plugin_modeladmin_cls = plugin_pool.plugins[plugin.type]
        plugin_model = plugin_modeladmin_cls.model
        plugin_modeladmin = plugin_modeladmin_cls(plugin_model, self.admin_site)

        extra_context = {
            'is_popup': True,
        }
        form_url = urlresolvers.reverse('admin:admin_edit_plugin', args=(pk, ))
        response = plugin_modeladmin.change_view(request, pk, form_url=form_url, extra_context=extra_context)

        if plugin_modeladmin.object_successfully_changed and not plugin_modeladmin.plugin_cke:
            return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')
        return response

    @never_cache
    def delete_plugin(self, request, pk):
        """
        Prompt delete form for requested plugin
        :param request:
        :param pk:
        :return: HTML (delete_view) or a script that close popup window
        """
        plugin = get_object_or_404(Plugin.objects, pk=pk)
        plugin_modeladmin_cls = plugin_pool.plugins[plugin.type]
        plugin_model = plugin_modeladmin_cls.model
        plugin_modeladmin = plugin_modeladmin_cls(plugin_model, self.admin_site)

        extra_context = {
            'is_popup': True,
            'delete_url': urlresolvers.reverse('admin:admin_delete_plugin', args=(pk, ))
        }
        response = plugin_modeladmin.delete_view(request, pk, extra_context=extra_context)

        if plugin_modeladmin.object_successfully_deleted:
            return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')
        return response

    @never_cache
    def select_plugin(self, request, pk):
        """
        Prompt custom select form for searching available plugins
        :param request:
        :param pk:
        :return: HTML (select form) or a script that close popup window
        """
        plugin = get_object_or_404(Plugin, pk=pk)

        if request.method == 'POST':
            form = SelectPluginForm(request.POST, plugin=plugin)
            if form.is_valid():
                selected_plugin = form.cleaned_data['plugin']
                selected_plugin.placeholder = plugin
                selected_plugin.save()

                return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')
        else:
            form = SelectPluginForm(plugin=plugin)

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            current_app=self.admin_site.name,
            form=form,
            is_popup=True,
            title=_('Select/Change plugin'),
            form_url=urlresolvers.reverse('admin:admin_select_plugin', args=(pk, ))
        )
        return render(request, 'admin/select_form.html', context)

    @never_cache
    def remove_plugin(self, request, pk):
        """
        Remove plugin from current placeholder
        :param request:
        :param pk:
        :return: None
        """
        if request.method == 'DELETE':
            plugin = get_object_or_404(Plugin, pk=pk)
            plugin.placeholder = None
            plugin.save()
            return HttpResponse()
        else:
            raise Http404

    @never_cache
    def move_plugin(self, request, pk):
        """
        Prompt custom move form for requested plugin
        :param request:
        :param pk:
        :return: HTML (move_form) or a script that close popup window
        """
        plugin = get_object_or_404(Plugin, pk=pk)

        if request.method == 'POST':
            form = MovePluginForm(request.POST, plugin=plugin)
            if form.is_valid():
                new_placeholder = form.cleaned_data['new_placeholder']
                new_page = form.cleaned_data['new_page']

                if new_page and plugin.type == 'RowPlugin':
                    row = plugin.row
                    row.page = new_page
                    if new_placeholder:
                        row.placeholder = new_placeholder
                    else:
                        row.placeholder = None
                    row.save()
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
            form_url=urlresolvers.reverse('admin:admin_move_plugin', args=(pk, ))
        )
        return render(request, 'admin/move_form.html', context)

    @never_cache
    def move_plugin_api(self, request, pk):
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

                        rows = Row.objects.filter(placeholder__isnull=False)\
                            .values_list('placeholder', flat=True)
                        plugins = Plugin.objects.filter(placeholder__isnull=False)\
                            .values_list('placeholder', flat=True)
                        columns = Column.objects.filter((Q(pk__in=rows) | ~Q(pk__in=plugins))
                                                               & ~Q(placeholder=plugin) & ~Q(pk=plugin.placeholder)
                                                               & Q(placeholder__row__page=page))\
                            .values('type', 'title', 'pk')
                    else:
                        rows = Row.objects.filter(placeholder__isnull=False)\
                            .values_list('placeholder', flat=True)
                        plugins = Plugin.objects.filter(placeholder__isnull=False)\
                            .values_list('placeholder', flat=True)
                        columns = Column.objects.filter((Q(pk__in=rows) | ~Q(pk__in=plugins))
                                                               & ~Q(placeholder=plugin) & ~Q(pk=plugin.placeholder))\
                            .values('type', 'title', 'pk')

                return JsonResponse(list(columns), safe=False)
            elif plugin.type == 'ColumnPlugin':
                if 'selected_page' in request.GET:
                    selected_page = request.GET['selected_page']
                    if selected_page:
                        page = get_object_or_404(HtmlPage, pk=selected_page)
                        rows = Row.objects.filter(page=page).exclude(pk=plugin.placeholder)\
                            .values('type', 'title', 'pk')
                    else:
                        rows = Row.objects.exclude(pk=plugin.placeholder)\
                            .values('type', 'title', 'pk')

                return JsonResponse(list(rows), safe=False)

admin.site.register(HtmlPage, HtmlPageAdmin)

