from django.core.urlresolvers import reverse
from django.test import TestCase

from learn.models import Dictionary, Translation


class ChooseExerciseTests(TestCase):
    def test_shouldReturnOneTranslation_FromASet(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown',
                                                 word_to_learn='TestLearn')
        url_parameters = {'dictionary_pk': dictionary.id}

        # When
        response = self.client.get(reverse('learn:choose_exercise', kwargs=url_parameters))

        # Then
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('learn:exercise', kwargs={
            'dictionary_pk': dictionary.id,
            'translation_pk': translation.id
        }))
