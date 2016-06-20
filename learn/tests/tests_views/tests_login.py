from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from learn.infrastructure.database import Database
from learn.views.comeback import come_back
from learn.views.login import login_view


class LoginTests(TestCase):
    @patch("learn.views.login.render")
    def test_shouldRedirectToLogin_WhenCalledWithGet(self, render_mock):
        # Given
        factory = RequestFactory()
        request = factory.get('fake-url')

        # When
        login_view(request)

        # Then
        expected_args = call(request, 'learn/login.html')
        self.assertEqual(render_mock.call_args_list[0], expected_args)

    @patch("learn.views.comeback.render")
    def test_shouldRender_WithNextRepetition_AndDictionary_AndLanguage(self, redirect_mock):
        # Given
        factory = RequestFactory()
        request = factory.get('fake-url')
        request.user = MagicMock(spec=AnonymousUser)
        request.user.is_authenticated.return_value = True
        database = MagicMock(Database)

        # When
        come_back(request, None, database=database)

        # Then
        expected_args = call(request, 'learn/come_back.html', context={
            'dictionary_pk': None,
            'language': database.get_dictionary_language(),
            'next_repetition': database.get_date_of_next_word_to_learn()})
        #self.assertEqual(redirect_mock.call_args_list[0], expected_args)
