from django.core.urlresolvers import reverse
from django.test import TestCase

from learn.models import Dictionary, Translation, RythmNotation
from learn.tests.tests_views.tests_int.utilities import create_and_login_a_user


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
                '<input placeholder="Translate the word!" id="answer" autocomplete="off" name="answer" type="text" class="validate" autofocus>',
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
                reverse('learn:choose_exercise',
                        kwargs={'dictionary_pk': dictionary.id, }) +
                '" class="waves-effect waves-light btn">Next</a>',
                response.content.decode('utf8'))

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
                """<input placeholder="Translate the word!" id="answer" autocomplete="off" name="answer" type="text" class="validate invalid" autofocus>""",
                response.content.decode('utf8'))
        self.assertInHTML(
                """<div class="card-panel red lighten-3">This field is required.</div>""",
                response.content.decode('utf8'))

    def test_shouldContainWordImportance(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown',
                                                 word_to_learn='TestLearn',
                                                 importance=Translation.SHOULD_KNOW)
        url_parameters = {'dictionary_pk': dictionary.id,
                          'translation_pk': translation.id}

        # When
        response = self.client.get(reverse('learn:exercise', kwargs=url_parameters))

        # Then
        self.assertInHTML("""<div class="col s12">
                            French (Should know):
                        </div>""", response.content.decode('utf8'))

    def test_shouldContainWordSuccesses_ForThisUser(self):
        # Given
        user = create_and_login_a_user(self.client)
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown',
                                                 word_to_learn='TestLearn',
                                                 importance=Translation.SHOULD_KNOW)
        RythmNotation.objects.create(translation=translation,
                                     user=user,
                                     successes=3)
        url_parameters = {'dictionary_pk': dictionary.id,
                          'translation_pk': translation.id}

        # When
        response = self.client.get(reverse('learn:exercise', kwargs=url_parameters))

        # Then
        self.assertInHTML('<div class="col s12 hide-on-small-only"><h5>How\'s this going ?</h5></div>',
                          response.content.decode('utf8'))
        self.assertInHTML('<div class="col s12"><b>Successes</b> : 3</div>',
                          response.content.decode('utf8'))
        self.assertInHTML('<div class="col s12"><b>Next repetition</b> : 31 seconds from now</div>',
                          response.content.decode('utf8'))

    def test_shouldNotContainWordSuccesses_WhenNotLoggedIn(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown',
                                                 word_to_learn='TestLearn',
                                                 importance=Translation.SHOULD_KNOW)
        url_parameters = {'dictionary_pk': dictionary.id,
                          'translation_pk': translation.id}

        # When
        response = self.client.get(reverse('learn:exercise', kwargs=url_parameters))

        # Then
        self.assertInHTML('<div class="col s2">Successes :</div>',
                          response.content.decode('utf8'), count=0)
