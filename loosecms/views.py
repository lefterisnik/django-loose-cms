# -*- coding: utf-8 -*-
from django.http import Http404
from django.core import urlresolvers
from django.shortcuts import redirect
from django.views.defaults import page_not_found
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language

from .models import *
from .utils.urls import *
from .utils.render import update_context


def _handle_no_page(request, page_slug, pages):
    """
    Handler for page creation
    """
    if request.user.is_authenticated() and request.user.is_staff:
        if page_slug.split('/')[0] in get_patterns():
            raise Http404

        template_pages = pages.filter(is_template=True)
        pages = pages.filter(is_template=False)
        context = dict(
            page_slug=page_slug,
            title=_('Edit page'),
            pages=pages,
            template_pages=template_pages
        )
        context = update_context(context)
        return render(request, 'admin/editor_form.html', context)
    else:
        raise Http404


def detail(request, page_slug, *args,  **kwargs):
    """
    Handles all requests
    Notice!!! page_slug doesn't contain language pref
    Context structure:
        redirect_to = represent the original user request without language prefix. We can't found because multiple
                      executions of this view so it must be passed to context
        pages = for the sidebar. Must be passed to context. From these we can found template pages and non.
        page = the page that user wants
            page_slug = we can found it from page
        examed = True if url was processed else False
        rows =  Row plugins that included in this page
        columns = Column plugins that included in above rows
        plugins = plugins that included in above columns
        other values contained in kwargs = If this view called from another urlconf

    """
    # Get all pages
    pages = kwargs.pop('pages', HtmlPage.objects.select_related('template').all())

    # Get page if this is the second run (double processing url) so page found in previous call
    page = kwargs.pop('page', None)

    # Tmp variable to determine if url processed or not
    # False: url not processed, True: url processed
    examed = kwargs.pop('examed', False)

    # Store the requested url for redirection if user wants multi language. It is used in menu plugin
    # TODO: Exam if is we needed to move to menu plugin
    redirect_to = kwargs.pop('redirect_to', None)

    # If there are not pages, redirect to login admin page to login and create some pages
    # Simulate first use
    if not pages:
        if not request.user.is_authenticated():
            return redirect(urlresolvers.reverse('admin:login') + '?next=' + request.path)

    # Exam url and find the last page in the url and call the appropriate view with extra kwargs
    if page_slug and '/' in page_slug and not examed:
        remaining_slug = None
        slugs = page_slug.split('/')

        # We could use also .reverse
        for counter, slug in enumerate(slugs):
            try:
                # recursively try to find the page
                slug = '/'.join(slugs[:len(slugs)-counter])
                page = pages.get(slug=slug)

                # We found the last page so get the other remaining slug  if exists to forward for resolving from
                # plugin url configurations
                if len(list(reversed(slugs))[:counter]) != 0:
                    # Gather the remaining url if exists
                    remaining_slug = '/%s/' % ('/'.join(slugs[len(slugs)-counter:]))
                break
            except HtmlPage.DoesNotExist:
                if counter == len(slugs)-1:
                    return _handle_no_page(request, page_slug, pages)
                continue

        # If remaining_slug exist
        if remaining_slug:
            # Fetch embed urls
            # TODO: Fetch only plugin url that appear to specific page
            embed_urlpatterns = get_app_urls(True)

            # Try to resolve the remaining slug
            view, args, kwargs = urlresolvers.resolve(remaining_slug, tuple(embed_urlpatterns))
            defaults = {
                'examed': True,
                'pages': pages,
                'page': page,
                'redirect_to': page_slug,
            }
            defaults.update(kwargs)

            # If regex found then try to return the view for the specific view. If 404 raised then return
            # _handle_no_page and pass the founded page page_slug
            try:
                # Run the view with the new slug we found and send already discovered values (pages & page)
                return view(request, page.slug, *args, **defaults)
            except Http404:
                # If 404 raised then run handle_no_page
                return _handle_no_page(request, page_slug, pages)
    elif not page_slug:
        # Exam if page exist else raise 404
        # Special view for home page
        try:
            page = pages.get(published=True, home=True)
        except HtmlPage.DoesNotExist:
            return _handle_no_page(request, page_slug, pages)
    else:
        # Exam if page exist else raise 404
        # Handle the request. This if handles the plugin view calls
        try:
            if not page:
                page = pages.get(published=True, slug=page_slug)
        except HtmlPage.DoesNotExist:
            return _handle_no_page(request, page_slug, pages)

    # If page is template page and user is anonymous raise 404
    if page.is_template and request.user.is_anonymous():
        raise Http404

    # Initialize context object. Create context dict that contain all kwargs
    context = dict(
        pages=pages,
        page=page,
        page_slug=page.slug,
        redirect_to=redirect_to if redirect_to else page.slug,
        **kwargs
    )

    # Update context with row, columns and plugins
    context = update_context(context, page)

    # Render page for anonymous users
    return page.render(request, context)


def error404(request):
    try:
        error_page = HtmlPage.objects.get(is_error=True)
    except HtmlPage.DoesNotExist:
        return page_not_found(request)

    context = dict(
        page=error_page
    )
    context = update_context(context, error_page)

    return error_page.render(request, context)