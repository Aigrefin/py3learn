from django.core.urlresolvers import reverse
from django.test import TestCase

from learn.models import Dictionary, Translation


class ValidateExerciseTests(TestCase):
    def test_shouldRedirect_ToBadInput_WhenMethodIsNotPost(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown',
                                                 word_to_learn='TestLearn')
        url_parameters = {'dictionary_pk': dictionary.id,
                          'translation_pk': translation.id}

        # When
        response = self.client.get(reverse('learn:validate_exercise', kwargs=url_parameters))

        # Then
        self.assertRedirects(response, reverse('learn:exercise_bad_input', kwargs={
            'dictionary_pk': dictionary.id,
            'translation_pk': translation.id,
            'bad_input': 'bad_input'
        }))

    def test_shouldRedirect_ToBadInput_WhenFormIsNotValid(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown',
                                                 word_to_learn='TestLearn')
        url_parameters = {'dictionary_pk': dictionary.id,
                          'translation_pk': translation.id}

        # When
        response = self.client.post(reverse('learn:validate_exercise', kwargs=url_parameters))

        # Then
        self.assertRedirects(response, reverse('learn:exercise_bad_input', kwargs={
            'dictionary_pk': dictionary.id,
            'translation_pk': translation.id,
            'bad_input': 'bad_input'
        }))

    def test_shouldRedirect_ToWrongAnswer_WhenAnswerDifferent_FromWordToLearn(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown',
                                                 word_to_learn='TestLearn')
        url_parameters = {'dictionary_pk': dictionary.id,
                          'translation_pk': translation.id}

        # When
        response = self.client.post(
                reverse('learn:validate_exercise', kwargs=url_parameters),
                data={'answer': 'AWrongAnswer'})

        # Then
        self.assertRedirects(response, reverse('learn:exercise_wrong_answer', kwargs={
            'dictionary_pk': dictionary.id,
            'translation_pk': translation.id,
            'wrong_answer': 'wrong_answer'
        }))

    def test_shouldRedirect_ToRandomiseExercise_WhenAnswerEqualsWordToLearn(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown',
                                                 word_to_learn='TestLearn')
        url_parameters = {'dictionary_pk': dictionary.id,
                          'translation_pk': translation.id}

        # When
        response = self.client.post(
                reverse('learn:validate_exercise', kwargs=url_parameters),
                data={'answer': 'TestLearn'})

        # Then
        self.assertRedirects(response, reverse('learn:randomise_exercise', kwargs={
            'dictionary_pk': dictionary.id
        }), target_status_code=302)
