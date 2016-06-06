from unittest import TestCase
from unittest.mock import patch, call, MagicMock

from django.test import RequestFactory

from learn.infrastructure.database import Database
from learn.views.wrong_answer import exercise_wrong_answer


class ExerciseWrongAnswerTests(TestCase):
    @patch("learn.views.wrong_answer.render")
    def test_shouldRenderWrongAnswer_WithDictionaryPK_AndTranslationPK_AndTranslation(self, render_mock):
        # Given
        database = MagicMock(Database)
        factory = RequestFactory()
        request = factory.get('fake-url')

        # When
        exercise_wrong_answer(request, 23, 42, database=database)

        # Then
        expected_args = call(request, 'learn/exercise_wrong_answer.html', context={
            'dictionary_pk': 23,
            'translation_pk': 42,
            'translation': database.get_translation()
        })
        self.assertEqual(render_mock.call_args_list[0], expected_args)
