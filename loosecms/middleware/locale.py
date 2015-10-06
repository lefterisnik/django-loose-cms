# -*- coding: utf-8 -*-
import re

from django.conf import settings
from django.utils import translation
from django.middleware.locale import LocaleMiddleware
from django.core.urlresolvers import LocaleRegexURLResolver
from django.utils.translation import get_language, get_language_from_path, get_language_from_request


class SimpleLocaleMiddleware(LocaleMiddleware):

    def process_request(self, request):
        if self.is_language_prefix_patterns_used():
            user_language = get_language_from_request(request, True)
            language = get_language_from_path(request.path_info)
            if not language and user_language in settings.LANGUAGE_CODE:
                language = settings.LANGUAGE_CODE
            else:
                language = user_language
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()


class NoPrefixLocaleRegexURLResolver(LocaleRegexURLResolver):

    @property
    def regex(self):
        language_code = get_language()
        if language_code not in self._regex_dict:
            regex_compiled = (re.compile('', re.UNICODE)
                              if language_code == settings.LANGUAGE_CODE
                              else re.compile('^%s/' % language_code, re.UNICODE))

            self._regex_dict[language_code] = regex_compiled
        return self._regex_dict[language_code]