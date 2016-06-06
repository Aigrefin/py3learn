from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from learn.infrastructure.database import Database
from learn.views.comeback import come_back


class ComebackTests(TestCase):
    @patch("learn.views.comeback.redirect")
    def test_shouldRedirectToDictionaries_IfNotAuthenticated(self, redirect_mock):
        # Given
        factory = RequestFactory()
        request = factory.get('fake-url')
        request.user = AnonymousUser()
        request.user.is_authenticated = False

        # When
        come_back(request, None, database=MagicMock(Database))

        # Then
        expected_args = call(request, 'learn:dictionaries')
        self.assertEqual(redirect_mock.call_args_list[0], expected_args)

    @patch("learn.views.comeback.render")
    def test_shouldRender_WithNextRepetition_AndDictionary_AndLanguage(self, redirect_mock):
        # Given
        factory = RequestFactory()
        request = factory.get('fake-url')
        request.user = AnonymousUser()
        request.user.is_authenticated = True
        database = MagicMock(Database)

        # When
        come_back(request, None, database=database)

        # Then
        expected_args = call(request, 'learn/come_back.html', context={
            'dictionary_pk': None,
            'language': database.get_dictionary_language(),
            'next_repetition': database.get_date_of_next_word_to_learn()})
        self.assertEqual(redirect_mock.call_args_list[0], expected_args)
