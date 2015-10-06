# -*- coding: utf-8 -*-
from django.http import Http404
from django.core import urlresolvers
from django.shortcuts import redirect
from django.views.defaults import page_not_found
from django.utils.translation import ugettext_lazy as _

from .models import *
from .utils.urls import *
from .utils.render import update_context


def _handle_no_page(request, pages, context):
    if request.user.is_authenticated() and request.user.is_staff:
        template_pages = pages.filter(is_template=True)
        pages = pages.filter(is_template=False)
        context.update(
            is_popup=True,
            template_pages=template_pages,
            pages=pages,
            title=_('Edit page'),
        )
        context = update_context(context)
        return render(request, 'admin/editor_form.html', context)
    else:
        raise Http404


def detail(request, page_slug, *args,  **kwargs):
    # Get all pages
    pages = HtmlPage.objects.select_related('template').all()

    # If there are not pages, redirect to login admin page to login and create some pages
    if not pages:
        if not request.user.is_authenticated():
            return redirect(urlresolvers.reverse('admin:login') + '?next=' + request.path)

    # Tmp variable to determine if calling is from plugin or from user request
    # False: user request, True: plugin request
    examed = kwargs.pop('examed', False)

    context = {}
    context['page_slug'] = page_slug

    # If this function called form another urlconf, send kwargs so pass it to context
    if kwargs:
        context['kwargs'] = kwargs

    # Exam url and find the last page in the url
    if page_slug and '/' in page_slug:
        remaining_slug = None
        slugs = page_slug.split('/')
        # We could use also .reverse
        for counter, slug in enumerate(slugs):
            try:
                slug = '/'.join(slugs[:len(slugs)-counter])
                page = pages.get(slug=slug)

                # if page was found will set the new page_slug
                page_slug = slug
                context['page_slug'] = page_slug

                # We find the last page so get the other remaining slug to forward for resolving to all plugins
                if len(list(reversed(slugs))[:counter]) != 0:
                    # Gather the remaining url if exists
                    remaining_slug = '/%s/' % ('/'.join(slugs[len(slugs)-counter:]))
                break
            except HtmlPage.DoesNotExist:
                if counter == len(slugs)-1:
                    return _handle_no_page(request, pages, context)
                continue

        # If page slug exist and remaining_slug exist and remaining_slug doesn't examed
        if remaining_slug:
            if not examed:
                # Fetch embed urls
                # TODO: Fetch only plugin url that appear to specific page
                embed_urlpatterns = get_app_urls(True)
                # Try to resolve the remaining slug
                view, args, kwargs = urlresolvers.resolve(remaining_slug, tuple(embed_urlpatterns))
                defaults = {
                    'examed': True,
                }
                defaults.update(kwargs)


                # If regex found then try to return the view for the specific view. If 404 raised then return
                # _handle_no_page and pass the original page_slug
                page_slug = '%s/%s' % (page_slug, remaining_slug.strip('/'))
                try:
                    return view(request, page_slug, *args, **defaults)
                except Http404:
                    context['page_slug'] = page_slug
                    return _handle_no_page(request, pages, context)
    elif not page_slug:
        # Exam if page exist else raise 404
        try:
            page = pages.get(published=True, home=True)
        except HtmlPage.DoesNotExist:
            return _handle_no_page(request, pages, context)
    else:
        try:
            page = pages.get(published=True, slug=page_slug)
        except HtmlPage.DoesNotExist:
            return _handle_no_page(request, pages, context)

    # If page is template page and user is anonymous raise 404
    if page.is_template and request.user.is_anonymous():
        raise Http404

    context['page'] = page
    context = update_context(context, page)

    # Render page for anonymous users
    return page.render(request, context)


def error404(request):
    try:
        error_page = HtmlPage.objects.get(is_error=True)
    except HtmlPage.DoesNotExist:
        return page_not_found(request)

    context = {}
    context['page'] = error_page
    context = update_context(context, error_page)

    return error_page.render(request, context)