from unittest import TestCase

from django.db import utils

from learn.models import Translation, Dictionary


class TranslationsTests(TestCase):
    def test_shouldNotAccept_TheSameKnownWordTwice(self):
        # Given
        dictionary = Dictionary.objects.create(language='testLang')
        Translation.objects.create(dictionary=dictionary, importance=Translation.NICE_TO_KNOW, known_word='known',
                                   word_to_learn='to_learn')

        # When
        try:
            Translation.objects.create(dictionary=dictionary, importance=Translation.NICE_TO_KNOW, known_word='known',
                                       word_to_learn='to_learn')
        except Exception as e:
            self.assertIsInstance(e, utils.IntegrityError)
