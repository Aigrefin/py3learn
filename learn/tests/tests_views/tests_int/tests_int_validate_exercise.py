from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.datetime_safe import datetime

from learn.models import Dictionary, Translation, RythmNotation
from learn.tests.tests_views.tests_int.utilities import create_and_login_a_user


def fake_next_repetition(successes):
    return datetime(2016, 1, 1, 1, 1, successes)


class ValidateExerciseTests(TestCase):
    def setUp(self):
        self.dictionary = Dictionary.objects.create(language='TestLang')
        self.translation = Translation.objects.create(dictionary=self.dictionary,
                                                      known_word='TestKnown',
                                                      word_to_learn='TestLearn')
        self.url_parameters = {'dictionary_pk': self.dictionary.id,
                               'translation_pk': self.translation.id}

    def test_shouldRedirect_ToBadInput_WhenMethodIsNotPost(self):
        # When
        response = self.client.get(reverse('learn:validate_exercise', kwargs=self.url_parameters))

        # Then
        self.assertRedirects(response, reverse('learn:exercise_bad_input', kwargs={
            'dictionary_pk': self.dictionary.id,
            'translation_pk': self.translation.id,
            'bad_input': 'bad_input'
        }))

    def test_shouldRedirect_ToBadInput_WhenFormIsNotValid(self):
        # When
        response = self.client.post(reverse('learn:validate_exercise', kwargs=self.url_parameters))

        # Then
        self.assertRedirects(response, reverse('learn:exercise_bad_input', kwargs={
            'dictionary_pk': self.dictionary.id,
            'translation_pk': self.translation.id,
            'bad_input': 'bad_input'
        }))

    def test_shouldRedirect_ToWrongAnswer_WhenAnswerDifferent_FromWordToLearn(self):
        # When
        response = self.client.post(
                reverse('learn:validate_exercise', kwargs=self.url_parameters),
                data={'answer': 'AWrongAnswer'})

        # Then
        self.assertRedirects(response, reverse('learn:exercise_wrong_answer', kwargs={
            'dictionary_pk': self.dictionary.id,
            'translation_pk': self.translation.id,
        }))

    def test_shouldRedirect_ToRandomiseExercise_WhenAnswerEqualsWordToLearn(self):
        # When
        response = self.client.post(
                reverse('learn:validate_exercise', kwargs=self.url_parameters),
                data={'answer': 'TestLearn'})

        # Then
        self.assertRedirects(response, reverse('learn:choose_exercise', kwargs={
            'dictionary_pk': self.dictionary.id
        }), target_status_code=302)

    def test_shouldRecordASuccess_ForTheCurrentTranslation_WhenSuccessfulyAnswered(self):
        # Given
        user = create_and_login_a_user(self.client)
        RythmNotation.objects.create(translation=self.translation,
                                     user=user,
                                     successes=0)

        # When
        self.client.post(
                reverse('learn:validate_exercise', kwargs=self.url_parameters),
                data={'answer': 'TestLearn'})

        # Then
        self.assertEqual(self.translation.rythmnotation_set.first().successes, 1)

    def test_shouldChangeNextRepetition_ForTheCurrentTranslation_WhenSuccessfulyAnswered(self):
        # Given
        user = create_and_login_a_user(self.client)
        notation = RythmNotation.objects.create(translation=self.translation,
                                     user=user,
                                     successes=0)
        current_repetition = notation.next_repetition

        # When
        self.client.post(
                reverse('learn:validate_exercise', kwargs=self.url_parameters),
                data={'answer': 'TestLearn'})

        # Then
        translation_repetition = self.translation.rythmnotation_set.first()
        self.assertNotEqual(translation_repetition.next_repetition, current_repetition)

    def test_shouldDowngradeNotation_ForTheCurrentTranslation_WhenFailedAnswered(self):
        # Given
        user = create_and_login_a_user(self.client)
        RythmNotation.objects.create(translation=self.translation,
                                     user=user,
                                     successes=8)

        # When
        self.client.post(
                reverse('learn:validate_exercise', kwargs=self.url_parameters),
                data={'answer': 'badAnswer'})

        # Then
        self.assertEqual(self.translation.rythmnotation_set.first().successes, 4)
