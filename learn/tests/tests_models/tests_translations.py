from django.test import TestCase

from learn.models import Translation, Dictionary


class TranslationsTests(TestCase):
    def test_shouldReturnDisplayableImportance(self):
        # Given
        dictionary = Dictionary.objects.create(language='testLang')
        translation = Translation.objects.create(dictionary=dictionary, importance=Translation.NICE_TO_KNOW)

        # When
        result = translation.get_importance_str()

        # Then
        self.assertEqual(result, 'Nice to know')
