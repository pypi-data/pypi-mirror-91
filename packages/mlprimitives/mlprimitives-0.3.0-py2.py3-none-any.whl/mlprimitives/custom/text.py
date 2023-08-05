import re

import iso639
import langdetect
import pandas as pd
from nltk.corpus import stopwords


class TextCleaner(object):
    RE_NON_ALPHA = re.compile(r'[^a-z]+')

    RE_SYMBOLS = re.compile(r'[-]')

    RE_NON_ALNUM = re.compile(r'[^\w\d]')

    RE_ACCENTS = {
        'a': re.compile(r'[àâáäåã]'),
        'e': re.compile(r'[èêéë]'),
        'i': re.compile(r'[ìîíï]'),
        'o': re.compile(r'[òôóö]'),
        'u': re.compile(r'[ùûúü]')
    }

    STOPWORDS = dict()

    def __init__(self, column=None, language='multi', lower=True, accents=True,
                 stopwords=True, non_alpha=True, single_chars=True):
        self.column = column
        self.language = language
        self.language_code = None

        self.lower = lower
        self.accents = accents
        self.stopwords = stopwords
        self.non_alpha = non_alpha
        self.single_chars = single_chars

    @staticmethod
    def detect_language(texts):
        texts = pd.Series(texts)
        language_codes = texts.apply(langdetect.detect).value_counts()
        return language_codes.index[0]

    def fit(self, X):
        if self.language == 'auto':
            if self.column:
                texts = X[self.column]
            else:
                texts = pd.Series(texts)

            self.language_code = self.detect_language(texts)

        elif self.language != 'multi':
            self.language_code = self.language

    @classmethod
    def _clean_accents(cls, text):
        for sub, regex in cls.RE_ACCENTS.items():
            text = regex.sub(sub, text)

        return text

    @classmethod
    def get_stopwords(cls, language_code):
        if language_code in cls.STOPWORDS:
            return cls.STOPWORDS[language_code]

        try:
            names = [lang.strip().lower() for lang in iso639.to_name(language_code).split(';')]
        except iso639.NonExistentLanguageError:
            return []

        for name in names:
            try:
                sw = stopwords.words(name)
                cls.STOPWORDS[language_code] = sw
                return sw

            except Exception:
                pass

        return []

    def _remove_stopwords(self, text):
        if text == '':
            return text

        if self.language_code:
            language_code = self.language_code

        elif self.language == 'multi':
            language_code = langdetect.detect(text)

        sw = self.get_stopwords(language_code)

        return ' '.join(word for word in text.split() if word not in sw)

    @classmethod
    def _remove_non_alpha(cls, text):
        text = cls.RE_SYMBOLS.sub('', text)
        text = cls.RE_NON_ALPHA.sub(' ', text)
        return ' '.join(text.split())

    @classmethod
    def _remove_single_chars(cls, text):
        words = text.split()
        return ' '.join(word for word in words if len(word) > 1)

    def produce(self, X):
        if self.column:
            texts = X[self.column]
        else:
            texts = pd.Series(X)

        texts = texts.fillna('')

        if self.lower:
            texts = texts.str.lower()

        if self.accents:
            texts = texts.apply(self._clean_accents)

        if self.stopwords:
            texts = texts.apply(self._remove_stopwords)

        if self.non_alpha:
            texts = texts.apply(self._remove_non_alpha)

        if self.single_chars:
            texts = texts.apply(self._remove_single_chars)

        if self.column:
            X = X.copy()
            X[self.column] = texts
            return X

        else:
            return texts
