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

        split_page_slug = context['page_slug'].split('/')
        if get_language() in split_page_slug:
            split_page_slug = split_page_slug[1]
        else:
            split_page_slug = split_page_slug[0]

        if split_page_slug in get_patterns():
            raise Http404

        return render(request, 'admin/editor_form.html', context)
    else:
        raise Http404


def detail(request, page_slug, *args,  **kwargs):
    # Get all pages
    pages = kwargs.get('pages', HtmlPage.objects.select_related('template').all())
    page = kwargs.get('page', None)

    # If there are not pages, redirect to login admin page to login and create some pages
    # Simulate first use
    if not pages:
        if not request.user.is_authenticated():
            return redirect(urlresolvers.reverse('admin:login') + '?next=' + request.path)

    # Tmp variable to determine if calling is from plugin or from user request
    # False: url not processing, True: url processing
    examed = kwargs.pop('examed', False)

    # Initialize context object
    context = {}
    context['page_slug'] = page_slug

    # If this function called form another urlconf, it sends probably extra kwargs so pass it to context
    if kwargs:
        context['kwargs'] = kwargs

    # Exam url and find the last page in the url and call the appropriate view with extra kwargs
    if page_slug and '/' in page_slug and not examed:
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

                # We found the last page so get the other remaining slug  if exists to forward for resolving from
                # plugin url configurations
                if len(list(reversed(slugs))[:counter]) != 0:
                    # Gather the remaining url if exists
                    remaining_slug = '/%s/' % ('/'.join(slugs[len(slugs)-counter:]))
                break
            except HtmlPage.DoesNotExist:
                if counter == len(slugs)-1:
                    return _handle_no_page(request, pages, context)
                continue

        # If page slug exist and remaining_slug exist
        if remaining_slug:
            # Fetch embed urls
            # TODO: Fetch only plugin url that appear to specific page
            embed_urlpatterns = get_app_urls(True)

            # Try to resolve the remaining slug
            view, args, kwargs = urlresolvers.resolve(remaining_slug, tuple(embed_urlpatterns))
            defaults = {
                'examed': True,
                'pages': pages,
                'page': page
            }
            defaults.update(kwargs)

            # If regex found then try to return the view for the specific view. If 404 raised then return
            # _handle_no_page and pass the original page_slug
            try:
                # Run the view with the new slug we found and send already discovered values (pages & page)
                return view(request, page_slug, *args, **defaults)
            except Http404:
                # If 404 raised then send the original slug
                page_slug = '%s/%s' % (page_slug, remaining_slug.strip('/'))
                context['page_slug'] = page_slug
                return _handle_no_page(request, pages, context)
    elif not page_slug:
        # Exam if page exist else raise 404
        # Special view for home page
        try:
            page = pages.get(published=True, home=True)
        except HtmlPage.DoesNotExist:
            return _handle_no_page(request, pages, context)
    else:
        # Exam if page exist else raise 404
        # Handle the request. This if handles the plugin view calls
        try:
            if not page:
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