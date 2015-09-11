# -*- coding: utf-8 -*-
import tinycss
from HTMLParser import HTMLParser


def populate_cssclasses_attrs(csss, plugin_style_inst):
    # For each css, parse it with tinycss and exam if id or class exist in them
    # and then take the attrs or declarations according to tinycss
    for css in csss:
        css_parser = tinycss.make_parser('page3')
        stylesheet = css_parser.parse_stylesheet_file(css)

        for html_tag in plugin_style_inst.html_tags:
            for rule in stylesheet.rules:
                if not rule.at_keyword:
                    for css_class in html_tag.classes:
                        if rule.selector.as_css().endswith(".%s" % css_class.name):
                            css_class.attrs[rule.selector.as_css()] = list(rule.declarations)
                    if rule.selector.as_css().endswith("#%s" % html_tag.id):
                        for declaration in rule.declarations:
                            html_tag.style += '%s: %s' % (declaration.name, declaration.value.as_css())


def get_initial_values(plugin_style_inst):
    return [get_dict(html_tag) for html_tag in plugin_style_inst.html_tags]


def get_dict(html_tag):
    return {
        'original_html': html_tag.original,
        'html_tag': html_tag.name,
        'html_id': html_tag.id,
        'styleclasses': get_styleclasses(html_tag),
        'css': html_tag.style,
        'position': html_tag.position
    }


def get_styleclasses(html_tag):
    defaults = []
    for class_ in html_tag.classes:
        try:
            styleclass = StyleClass.objects.get(title=class_.name, override=False)
            # TODO: if override is False then user don't change it (add extra attrs )
            # so it is safe to update class attrs
        except StyleClass.DoesNotExist:
            styleclass = StyleClass(title=class_.name, from_source=True)
            styleclass.save()

        for attr in class_.attrs:

            css = '%s\n' % ('\n'.join(x.name + ": " + x.value.as_css() + ";" for x in class_.attrs[attr]))
            try:
                styleclassinherit = StyleClassInherit.objects.get(title=attr)
            except StyleClassInherit.DoesNotExist:
                styleclassinherit = StyleClassInherit(title=attr, css=css,
                                                      styleclass=styleclass)
                styleclassinherit.save()

        defaults.append(styleclass)

    return [x.pk for x in defaults]


## Classes for the parsing html plugin's template

class PluginStyle(object):
    def __init__(self, html_tags=None, css_classes=None):
        if html_tags is None:
            self.html_tags = []
        else:
            self.html_tags = html_tags

    def exam_if_tag_exist(self, htmltag_inst):
        if len(self.html_tags) != 0:
            for html_tag in self.html_tags:
                if html_tag.name == htmltag_inst.name and \
                                html_tag.classes == htmltag_inst.classes and \
                                html_tag.id == htmltag_inst.id:
                    html_tag.update_position(htmltag_inst.position)
                    return True
        return False

    def exam_if_class_exist(self, class_name):
        for html_tag in self.html_tags:
            for css_class in html_tag.classes:
                if class_name == css_class.name:
                    return css_class
        return False


class CssClass(object):
    def __init__(self, name, attrs=None):
        self.name = name
        if attrs is None:
            self.attrs = dict()
        else:
            self.attrs = attrs


class HtmlTag(object):
    def __init__(self, name, original=None, position=None, id=None, classes=None, style=""):
        self.name, self.id, self.style, self.original = name, id, style, original
        if classes is None:
            self.classes = []
        else:
            self.classes = classes

        if position is None:
            self.position = ()
        else:
            self.position = position

    def add_class_inst(self, class_inst):
        self.classes.append(class_inst)

    def set_id(self, id_name):
        self.id = id_name

    def set_style(self, style):
        self.style = style

    def update_position(self, position):
        if isinstance(self.position, tuple):
            self.position = [self.position]
        self.position.append(position)


class MyHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.plugin_style = PluginStyle()

    def handle_starttag(self, tag, attrs):
        html_tag = HtmlTag(name=tag, position=self.getpos())
        html_tag.original = self.get_starttag_text()

        for attr in attrs:
            if attr[0] == 'class':
                for class_ in attr[1].split():
                    exist = self.plugin_style.exam_if_class_exist(class_)
                    if not exist :
                        css_class = CssClass(name=class_)
                        html_tag.add_class_inst(css_class)
                    else:
                        html_tag.add_class_inst(exist)
            if attr[0] == 'id':
                html_tag.set_id(attr[1])
            if attr[0] == 'style':
                html_tag.set_style(attr[1])


        if not self.plugin_style.exam_if_tag_exist(html_tag):
            self.plugin_style.html_tags.append(html_tag)