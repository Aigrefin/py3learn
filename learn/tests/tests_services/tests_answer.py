from unittest import TestCase
from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
from django.utils import timezone

from learn.infrastructure.database import Database
from learn.models import Translation, RythmNotation
from learn.services.answer import Answer


class AnswerTests(TestCase):
    def setUp(self):
        self.database = MagicMock(spec=Database)
        self.answer = Answer(database=self.database)
        self.user = User()

    def test_shouldReturnTrue_WhenGoodAnswer(self):
        # Given
        translation = Translation(word_to_learn="Xin chào", known_word="Bonjour")

        # When
        result = self.answer.is_good_answer("xin chào", translation)

        # Then
        self.assertTrue(result)

    def test_shouldReturnFalse_WhenBadAnswer(self):
        # Given
        translation = Translation(word_to_learn="Xin chào", known_word="Bonjour")

        # When
        result = self.answer.is_good_answer("xin chao", translation)

        # Then
        self.assertFalse(result)

    def test_shouldRetreiveNotation_FromTranslation_AndUser(self):
        # Given
        translation = Translation(word_to_learn="Xin chào", known_word="Bonjour")

        # When
        self.answer.update_translation_statistics(True, self.user, translation)

        # Then
        self.assertEqual(self.database.get_matching_notation.call_args_list[0][0][0], self.user)
        self.assertEqual(self.database.get_matching_notation.call_args_list[0][0][1], translation)

    @patch('learn.services.answer.compute_next_repetition')
    def test_shouldImproveTranslationStatistics_WhenGoodAnswer(self, compute_next_repetition_mock):
        # Given
        translation = Translation(word_to_learn="Xin chào", known_word="Bonjour")
        notation = RythmNotation(translation=translation, successes=0, next_repetition=None)

        self.database.get_matching_notation.return_value = notation

        next_repetition = timezone.now()
        compute_next_repetition_mock.return_value = next_repetition

        # When
        self.answer.update_translation_statistics(True, self.user, translation)

        # Then
        self.assertEqual(self.database.save_rythm_notation.call_args_list[0][0][0], next_repetition)
        self.assertEqual(self.database.save_rythm_notation.call_args_list[0][0][1], 1)

    @patch('learn.services.answer.compute_next_repetition')
    def test_shouldDowngradeTranslationStatistics_WhenBadAnswer(self, compute_next_repetition_mock):
        # Given
        translation = Translation(word_to_learn="Xin chào", known_word="Bonjour")
        notation = RythmNotation(translation=translation, successes=42, next_repetition=None)

        self.database.get_matching_notation.return_value = notation

        next_repetition = timezone.now()
        compute_next_repetition_mock.return_value = next_repetition

        # When
        self.answer.update_translation_statistics(False, self.user, translation)

        # Then
        self.assertEqual(self.database.save_rythm_notation.call_args_list[0][0][0], next_repetition)
        self.assertEqual(self.database.save_rythm_notation.call_args_list[0][0][1], 21)
