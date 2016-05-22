from django.core.urlresolvers import reverse
from django.test import TestCase

from learn.models import Dictionary, Translation


class ExerciseTests(TestCase):
    def test_shouldRenderExercise_WithAnswerInput_WhenNominalCase(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown',
                                                 word_to_learn='TestLearn')
        url_parameters = {'dictionary_pk': dictionary.id,
                          'translation_pk': translation.id}

        # When
        response = self.client.get(reverse('learn:exercise', kwargs=url_parameters))

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
                """<div class="col s12 card-panel">
                    <p>TestKnown</p>
                </div>""",
                response.content.decode('utf8'))
        self.assertInHTML(
                '<input placeholder="Translate the word!" id="answer" name="answer" type="text" class="validate">',
                response.content.decode('utf8'))
        """self.assertInHTML(
                '<form class="col s12" action="' +
                reverse('learn:validate_exercise',
                        kwargs={'dictionary_pk': dictionary.id,
                                'translation_pk': translation.id}) +
                '" method="post"></form>',
                response.content.decode('utf8'))"""
        self.assertInHTML(
                '<a href="' +
                reverse('learn:randomise_exercise',
                        kwargs={'dictionary_pk': dictionary.id, }) +
                '" class="waves-effect waves-light btn">Next</a>',
                response.content.decode('utf8'))

    def test_shouldRenderExercise_WithoutAnswerInput_WithAnswerText_WhenWrongAnswer(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown',
                                                 word_to_learn='TestLearn')
        url_parameters = {'dictionary_pk': dictionary.id,
                          'translation_pk': translation.id,
                          'wrong_answer': 'wrong_answer'}

        # When
        response = self.client.get(reverse('learn:exercise_wrong_answer', kwargs=url_parameters))

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
                """<div class="col s12 card-panel">
                    <p>TestKnown</p>
                </div>""",
                response.content.decode('utf8'))
        self.assertInHTML(
                """<div class="col s12 card-panel green lighten-3">
                    <p>TestLearn</p>
                </div>""",
                response.content.decode('utf8'))
        self.assertInHTML(
                '<input placeholder="Translate the word!" id="answer" name="answer" type="text" class="validate">',
                response.content.decode('utf8'), count=0)

    def test_shouldRenderExercise_WithAnswerInput_WithBadInputText_WhenBadInput(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown',
                                                 word_to_learn='TestLearn')
        url_parameters = {'dictionary_pk': dictionary.id,
                          'translation_pk': translation.id,
                          'bad_input': 'bad_input'}

        # When
        response = self.client.get(reverse('learn:exercise_bad_input', kwargs=url_parameters))

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
                """<div class="col s12 card-panel">
                    <p>TestKnown</p>
                </div>""",
                response.content.decode('utf8'))
        self.assertInHTML(
                """<input placeholder="Translate the word!" id="answer" name="answer" type="text" class="validate invalid">""",
                response.content.decode('utf8'))
        self.assertInHTML(
                """<div class="card-panel red lighten-3">This field is required.</div>""",
                response.content.decode('utf8'))
