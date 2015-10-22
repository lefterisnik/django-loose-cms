# -*- coding: utf-8 -*-
# Helpful: objects.create call save function but Plugin() don't call it.
# Helpful: with request context processor many GET, POST variable passed to context
# which can used in templates or other plugins. Each context processor can define new
# variables which can used in views or middlewares.
from django.contrib.auth import get_user_model
from loosecms.models import HtmlPage, Row, Column


def create_page(title='Page', slug='page', is_template=False, is_error=False, home=False):
    htmlpage = HtmlPage.objects.create(title=title, slug=slug, is_template=is_template,
                                       is_error=is_error, home=home)
    return htmlpage


def create_row_plugin(page, placeholder=None, title='Row', slug='row', order=0):
    row = Row.objects.create(placeholder=None, title=title, slug=slug, page=page, order=order)
    return row


def create_column_plugin(placeholder=None, title='Column', slug='column', width=12, order=0):
    column = Column.objects.create(placeholder=placeholder, title=title, slug=slug, width=width,
                                   order=order)
    return column


def create_admin_user(username='admin', email='', password='admin'):
    get_user_model().objects.create_superuser(username=username, email=email, password=password)