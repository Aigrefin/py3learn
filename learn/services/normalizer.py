import re


class TranslationNormalizer:
    def __normalize_string(self, string):
        return re.sub(r'\s+', r' ', string).strip()

    def normalize_translation(self, translation_to_normalize):
        translation_to_normalize.word_to_learn = self.__normalize_string(translation_to_normalize.word_to_learn)
        translation_to_normalize.known_word = self.__normalize_string(translation_to_normalize.known_word)
        return translation_to_normalize
