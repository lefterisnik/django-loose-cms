# -*- coding: utf-8 -*-
# Helpful: objects.create call save function but Plugin() don't call it.
# Helpful: with request context processor many GET, POST variable passed to context
# which can used in templates or other plugins. Each context processor can define new
# variables which can used in views or middlewares.
from loosecms.models import HtmlPage, Row, Column


def create_page(is_template=False):
    htmlpage = HtmlPage.objects.create(title='page1',
                                       slug='page1',
                                       is_template=is_template)
    return htmlpage


def create_row_plugin(htmlpage):
    row = Row.objects.create(title='row1',
                             slug='row1',
                             page=htmlpage,
                             order=0)
    return row


def create_column_plugin(placeholder):
    column = Column.objects.create(title='column1',
                                    slug='column1',
                                    width='12',
                                    placeholder=placeholder)
    return column



def create_404_page():
    htmlpage = HtmlPage.objects.create(title='page404',
                                       slug='page404',
                                       is_error=True)
    return htmlpage