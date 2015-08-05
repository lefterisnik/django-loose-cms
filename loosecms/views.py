# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.core import urlresolvers
from django.http import Http404
from django.views.defaults import page_not_found

from .models import *
from .utils import *


def detail(request, page_slug, *args,  **kwargs):
    # Get all pages
    pages = Page.objects.select_related('htmlpage', 'syndicationpage').all()

    context = {}
    context['page_slug'] = page_slug

    # If this function called form another urlconf, send kwargs so pass it to context
    if kwargs:
        context['kwargs'] = kwargs

    # If there are not pages, redirect to login admin page to login
    if not pages:
        if not request.user.is_authenticated():
            return redirect(urlresolvers.reverse('admin:index'))

    # Exam if page exist else raise 404
    try:
        if not page_slug:
            page = pages.get(published=True, htmlpage__home=True)
        else:
            page = pages.get(published=True, slug=page_slug)

        if page.htmlpage.is_template and request.user.is_anonymous():
            raise Http404
    except Page.DoesNotExist:
        if request.user.is_authenticated() and request.user.is_staff:
            template_pages = pages.filter(htmlpage__is_template=True)
            pages = pages.filter(htmlpage__is_template=False)
            context.update(
                is_popup=True,
                template_pages=template_pages,
                pages=pages,
            )
            context = update_context(context)
            return render(request, 'admin/editor_lite.html', context)
        else:
            raise Http404

    # TODO: add control to exam what type is
    page = page.htmlpage
    context['page'] = page
    context = update_context(context, page)
    context['styles'] = Style.objects.all().prefetch_related('styleclasses')

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