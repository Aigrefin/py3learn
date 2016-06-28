from django.contrib.auth.models import User
from django.test import TestCase

from learn.models import Dictionary, Translation
from learn.services.choice import rythm_choice


class ChooseRythmNotationExerciseIntTests(TestCase):
    def test_shouldReturnWord(self):
        # Given
        user = User.objects.create()
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(known_word='test_known', word_to_learn='test_learn', dictionary=dictionary)

        # When
        result = rythm_choice(dictionary, user)

        # Then
        self.assertEqual(result, translation)
