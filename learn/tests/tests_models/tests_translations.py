from unittest import TestCase

from learn.models import Translation, Dictionary


class TranslationsTests(TestCase):
    def test_shouldReturnDisplayableImportance(self):
        # Given
        dictionary = Dictionary(language='testLang')
        translation = Translation(dictionary=dictionary, importance=Translation.NICE_TO_KNOW)

        # When
        result = translation.get_importance_str()

        # Then
        self.assertEqual(result, 'Nice to know')

    def test_shouldDisplayKnownWord_AsStr(self):
        # Given
        dictionary = Dictionary(language='testLang')
        translation = Translation(dictionary=dictionary, importance=Translation.NICE_TO_KNOW, known_word='known',
                                  word_to_learn='to_learn')

        # When
        result = str(translation)

        # Then
        self.assertEqual(result, 'known')
