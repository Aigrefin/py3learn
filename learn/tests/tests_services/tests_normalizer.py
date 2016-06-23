from unittest import TestCase

from learn.models import Translation
from learn.services.normalizer import TranslationNormalizer


class TranslationNormalizerTests(TestCase):
    def test_thatShouldStripTheWordsOfATranslation(self):
        # Given
        normalizer = TranslationNormalizer()
        translation_to_normalize = Translation()
        translation_to_normalize.word_to_learn = "  test to learn "
        translation_to_normalize.known_word = " test known  "

        # When
        normalizer.normalize_translation(translation_to_normalize)

        # Then
        self.assertEqual(translation_to_normalize.word_to_learn, "test to learn")
        self.assertEqual(translation_to_normalize.known_word, "test known")

    def test_thatShouldReplaceConsecutiveSpacesByOne(self):
        # Given
        normalizer = TranslationNormalizer()
        translation_to_normalize = Translation()
        translation_to_normalize.word_to_learn = "test  to      learn"
        translation_to_normalize.known_word = "test     known"

        # When
        normalizer.normalize_translation(translation_to_normalize)

        # Then
        self.assertEqual(translation_to_normalize.word_to_learn, "test to learn")
        self.assertEqual(translation_to_normalize.known_word, "test known")

    def test_thatShouldReturnTheSameTranslationObject(self):
        # Given
        normalizer = TranslationNormalizer()
        translation_to_normalize = Translation()

        # When
        result = normalizer.normalize_translation(translation_to_normalize)

        # Then
        self.assertEqual(result, translation_to_normalize)
