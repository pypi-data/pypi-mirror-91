# -*- coding: utf-8 -*-
"""
A Translation module.

You can translate text using this module.
"""
import json
import requests
import unidecode
from pygoogletranslation import utils, urls
from pygoogletranslation.constants import (
    LANGCODES, LANGUAGES, RPCIDS
)
from pygoogletranslation import gauthtoken
from pygoogletranslation.models import Translated, Detected


class Translator:

    def __init__(self, host=urls.TRANSLATE, proxies=None, timeout=None):
        self.host = host if 'http' in host else 'https://' + host
        self.rpcids = RPCIDS
        self.transurl = urls.TRANSLATEURL
        if proxies is not None:
            self.proxies = proxies
        else:
            self.proxies = None
        
        if timeout is not None:
            self.timeout = timeout

    def translate(self, text, src='auto', dest='en'):

        if src != 'auto':
            if src in LANGCODES:
                src = LANGCODES[src]
            elif src in LANGUAGES:
                src = src
            else:
                raise ValueError('invalid source language')

        if dest != 'en':
            if dest in LANGCODES:
                print(LANGCODES)
                dest = LANGCODES[src]
                print(dest)
            elif dest in LANGUAGES:
                dest = dest
            else:
                raise ValueError('invalid destination language')

        data = self._translate(text, src=src, dest=dest)
        # print(data)
        translated = data[0][2][1][0][0][5][0][0]
        extra_data = {}
        try:
            src = data[0][2][3][5][0][0][3]
        except Exception:  # pragma: nocover
            pass

        try:
            dest = data[0][2][3][5][0][0][2]
        except Exception:  # pragma: nocover
            pass

        pron = None
        try:
            pron = unidecode.unidecode(data[0][2][1][0][0][1])
        except Exception:  # pragma: nocover
            pass

        # put final values into a new Translated object
        result = Translated(src=src, dest=dest, origin=text,
                            text=translated, pronunciation=pron, extra_data=extra_data)
        return result

    def detect(self, text, **kwargs):
        """Detect language of the input text

        :param text: The source text(s) whose language you want to identify.
                     Batch detection is supported via sequence input.
        :type text: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)

        :rtype: Detected
        :rtype: :class:`list` (when a list is passed)

        Basic usage:
            >>> from googletrans import Translator
            >>> translator = Translator()
            >>> translator.detect('이 문장은 한글로 쓰여졌습니다.')
            <Detected lang=ko confidence=0.27041003>
            >>> translator.detect('この文章は日本語で書かれました。')
            <Detected lang=ja confidence=0.64889508>
            >>> translator.detect('This sentence is written in English.')
            <Detected lang=en confidence=0.22348526>
            >>> translator.detect('Tiu frazo estas skribita en Esperanto.')
            <Detected lang=eo confidence=0.10538048>

        Advanced usage:
            >>> langs = translator.detect(['한국어', '日本語', 'English', 'le français'])
            >>> for lang in langs:
            ...    print(lang.lang, lang.confidence)
            ko 1
            ja 0.92929292
            en 0.96954316
            fr 0.043500196
        """
        if isinstance(text, list):
            result = []
            for item in text:
                lang = self.detect(item)
                result.append(lang)
            return result

        data = self._translate(text, 'auto', 'en')

        # actual source language that will be recognized by Google Translator when the
        # src passed is equal to auto.
        src = ''
        confidence = 0.0
        try:
            src = data[0][2][3][5][0][0][3]
            # confidence = data[8][-2][0]
        except Exception:  # pragma: nocover
            pass
        result = Detected(lang=src, confidence=confidence)

        return result
        

    def _parse_extra_data(self, data):
        response_parts_name_mapping = {
            0: 'translation',
            1: 'all-translations',
            2: 'original-language',
            5: 'possible-translations',
            6: 'confidence',
            7: 'possible-mistakes',
            8: 'language',
            11: 'synonyms',
            12: 'definitions',
            13: 'examples',
            14: 'see-also',
        }

        extra = {}

        for index, category in response_parts_name_mapping.items():
            extra[category] = data[index] if (index < len(data) and data[index]) else None

        return extra
    
    def _translate(self, text, src, dest):
        """ Generate Token for each Translation and post requset to
        google web api translation and return an response

        If the status code is 200 the request is considered as an success
        else other status code are consider as translation failure.

        """
        url = self.transurl
        params = utils.format_param(self.rpcids)
        data = utils.format_data(self.rpcids, text, src, dest)
        response = requests.request("POST", url, data=data, params=params)
        if response.status_code == 200:
            _format_data = utils.format_response(str(response.text))
            return _format_data
        else:
            raise Exception('Unexpected status code {} from {}'.format(response.status_code, self.host))
            return False

    
    def glanguage(self):
        """ Get request from google and return language and their lang codes.

        Example:
        >>> translate = Translator()
        >>> translate.glanguage()
        >>> {
                "sl": {
                    "auto": "Detect language",
                    "af": "Afrikaans",
                    "sq": "Albanian",
                },
                "tl": {
                    "af": "Afrikaans",
                    "sq": "Albanian",
                    "am": "Amharic",
                    "ar": "Arabic",
                },
                "al": {}
            }
        """

        querystring = utils.format_querystringlang()
        response = requests.get(url=self.host + 'l', params=querystring, proxies=self.proxies)
        if response.status_code == 200:
            glang = json.loads(response.content)
            return glang
        else:
            raise Exception('Unexpected status code {} from {}'.format(response.status_code, self.host))
            return False
        
        
