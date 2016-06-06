from unittest import TestCase
from unittest.mock import patch, call, MagicMock

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.test import RequestFactory

from learn.models import Translation
from learn.services.choice import rythm_choice, random_choice
from learn.views.choose_exercise import choose_rythm_notation_exercise


class ChooseExerciseTests(TestCase):
    @patch("learn.views.choose_exercise.rythm_choice", spec=rythm_choice)
    @patch("learn.views.choose_exercise.redirect", spec=redirect)
    def test_shouldRedirectToExercise_WithRythmChoice_WhenUserAuthenticated(self, redirect_mock, rythm_choice_mock):
        # Given
        factory = RequestFactory()
        request = factory.get('fake-url')
        request.user = MagicMock(spec=AnonymousUser)
        request.user.is_authenticated.return_value = True

        choosen_translation = MagicMock(spec=Translation)
        choosen_translation.id = 12
        rythm_choice_mock.return_value = choosen_translation

        # When
        choose_rythm_notation_exercise(request, 42)

        # Then
        expected_args = call('learn:exercise', dictionary_pk=42, translation_pk=12)
        self.assertEqual(redirect_mock.call_args_list[0], expected_args)

    @patch("learn.views.choose_exercise.random_choice", spec=random_choice)
    @patch("learn.views.choose_exercise.redirect", spec=redirect)
    def test_shouldRedirectToExercise_WithRandomChoice_WhenUserAuthenticated(self, redirect_mock, random_choice_mock):
        # Given
        factory = RequestFactory()
        request = factory.get('fake-url')
        request.user = MagicMock(spec=AnonymousUser)
        request.user.is_authenticated.return_value = False

        choosen_translation = MagicMock(spec=Translation)
        choosen_translation.id = 12
        random_choice_mock.return_value = choosen_translation

        # When
        choose_rythm_notation_exercise(request, 42)

        # Then
        expected_args = call('learn:exercise', dictionary_pk=42, translation_pk=12)
        self.assertEqual(redirect_mock.call_args_list[0], expected_args)

    @patch("learn.views.choose_exercise.random_choice", spec=random_choice)
    @patch("learn.views.choose_exercise.rythm_choice", spec=rythm_choice)
    @patch("learn.views.choose_exercise.redirect", spec=redirect)
    def test_shouldRedirectToComeBack_WhenNoTranslation(self, redirect_mock, rythm_choice_mock, random_choice_mock):
        # Given
        factory = RequestFactory()
        request = factory.get('fake-url')
        request.user = MagicMock(spec=AnonymousUser)

        random_choice_mock.return_value = None
        rythm_choice_mock.return_value = None

        # When
        choose_rythm_notation_exercise(request, 42)

        # Then
        expected_args = call('learn:come_back', dictionary_pk=42)
        self.assertEqual(redirect_mock.call_args_list[0], expected_args)