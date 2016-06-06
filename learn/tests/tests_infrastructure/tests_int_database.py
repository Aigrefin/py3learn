from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.utils.datetime_safe import datetime

from learn.infrastructure.database import Database
from learn.models import Translation, RythmNotation, Dictionary


class DatabaseIntTests(TestCase):
    def setUp(self):
        self.user = User.objects.create()
        self.now = timezone.make_aware(datetime(2016, 4, 8, 15, 16, 23, 42))
        self.database = Database()
        self.dictionary = Dictionary.objects.create(language='English')

    def test_shouldReturnOrderedPlannedWordsToLearnBeforeNow(self):
        # Given
        translation = Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello', known_word='salut')
        translation2 = Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello2',
                                                  known_word='salut2')

        repetition_set_before_now = self.now.replace(2015)
        repetition_set_after_now = self.now.replace(2017)
        create_rythm_object(repetition_set_before_now, translation, self.user)
        create_rythm_object(repetition_set_after_now, translation2, self.user)

        # When
        result = self.database.get_ordered_scheduled_words_to_learn_before_date(self.now, self.dictionary.id, self.user)

        # Then
        self.assertIn(translation, result)
        self.assertNotIn(translation2, result)

    def test_shouldReturnWords_WithoutRythmNotation_ForThis_User(self):
        # Given
        translation = Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello', known_word='salut')
        translation2 = Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello2',
                                                  known_word='salut2')
        create_rythm_object(self.now, translation2, self.user)
        quantity_of_words_to_plan = 2

        # When
        result = self.database.get_unseen_words(self.dictionary.id, quantity_of_words_to_plan, self.user)

        # Then
        self.assertIn(translation, result)
        self.assertNotIn(translation2, result)

    def test_shouldReturnNoMoreWords_ThanAskedQuantity(self):
        # Given
        Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello', known_word='salut')
        Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello2', known_word='salut2')
        Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello3', known_word='salut3')
        Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello4', known_word='salut4')
        quantity_of_words_to_plan = 2

        # When
        result = self.database.get_unseen_words(self.dictionary.id, quantity_of_words_to_plan, self.user)

        # Then
        self.assertEqual(len(result), quantity_of_words_to_plan)

    def test_shouldCreateRythmNotation_ForThisUser_AndTranslation(self):
        # Given
        translations = list()
        translations.append(
                Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello', known_word='salut'))

        # When
        self.database.schedule_words(translations, self.user, self.now)

        # Then
        rythm_notations = RythmNotation.objects.filter(user=self.user)
        self.assertIn(rythm_notations[0], translations[0].rythmnotation_set.all())

    def test_shouldReturnTranslationMatchingTheId(self):
        # Given
        translation_id = 66
        Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello', known_word='salut',
                                   id=translation_id)

        # When
        result = self.database.get_translation(translation_id)

        # Then
        self.assertEqual(result.id, translation_id)

    def test_shouldReturnMatchingRythmNotation(self):
        # Given
        translation = Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello', known_word='salut')
        notation = create_rythm_object(self.now, translation, self.user)

        # When
        result = self.database.get_matching_notation(self.user, translation)

        # Then
        self.assertEqual(result, notation)

    def test_shouldPersist_NotationData(self):
        # Given
        translation = Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello', known_word='salut')
        notation = create_rythm_object(self.now, translation, self.user)
        next_repetition = timezone.now().replace(year=1442)

        # When
        self.database.save_rythm_notation(next_repetition, 42, notation)

        # Then
        notation = RythmNotation.objects.all().first()
        self.assertEqual(notation.successes, 42)
        self.assertEqual(notation.next_repetition, next_repetition)

    def test_shouldReturnDateOfNextWordToLearn(self):
        # Given
        translation1 = Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello', known_word='salut')
        translation2 = Translation.objects.create(dictionary=self.dictionary, word_to_learn='hello2', known_word='salut2')
        now = timezone.now()
        create_rythm_object(now, translation1, self.user)
        create_rythm_object(now + timedelta(seconds=10), translation2, self.user)

        # When
        result = self.database.get_date_of_next_word_to_learn(self.user)

        # Then
        self.assertEqual(result, now)


def create_rythm_object(repetition_set_after_now, translation2, user):
    rythm_notation = RythmNotation.objects.create(translation=translation2, user=user, successes=0)
    rythm_notation.next_repetition = repetition_set_after_now
    rythm_notation.save()
    return rythm_notation
