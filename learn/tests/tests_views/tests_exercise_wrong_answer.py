from django.core.urlresolvers import reverse
from django.test import TestCase

from learn.models import Dictionary
from learn.models import Translation


class ExerciseWrongAnswerTests(TestCase):
    def setUp(self):
        self.dictionary = Dictionary.objects.create(language='TestLang')
        self.translation = Translation.objects.create(dictionary=self.dictionary,
                                                      known_word='TestKnown',
                                                      word_to_learn='TestLearn',
                                                      importance=Translation.SHOULD_KNOW)
        self.url_parameters = {'dictionary_pk': self.dictionary.id,
                               'translation_pk': self.translation.id}

    def test_shouldRenderExercise_WithAnswerText(self):
        # When
        response = self.client.get(reverse('learn:exercise_wrong_answer', kwargs=self.url_parameters))

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
                """<div class="col s12 card-panel green lighten-3">
                    <p>TestLearn</p>
                </div>""",
                response.content.decode('utf8'))

    def test_shouldContainKnownWord(self):
        # When
        response = self.client.get(reverse('learn:exercise_wrong_answer', kwargs=self.url_parameters))

        # Then
        self.assertInHTML(
                """<div class="col s12 card-panel">
                    <p>TestKnown</p>
                </div>""",
                response.content.decode('utf8'))

    def test_shouldContainWordImportance(self):
        # When
        response = self.client.get(reverse('learn:exercise_wrong_answer', kwargs=self.url_parameters))

        # Then
        self.assertInHTML("""<div class="col s12">
                                French (Should know):
                            </div>""", response.content.decode('utf8'))
