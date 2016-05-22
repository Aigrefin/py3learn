from django.core.urlresolvers import reverse
from django.test import TestCase

from learn.models import Dictionary, Translation


class LearnViewsTests(TestCase):
    def test_shouldReturn_OrderedDictionaries(self):
        # Given
        Dictionary.objects.create(language='TestLang3')
        Dictionary.objects.create(language='TestLang1')
        Dictionary.objects.create(language='TestLang2')

        # When
        response = self.client.get(reverse('learn:dictionaries'))

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['dictionaries_list']),
                                 ['<Dictionary: TestLang1>',
                                  '<Dictionary: TestLang2>',
                                  '<Dictionary: TestLang3>'],
                                 ordered=True)

    def test_shouldReturnTranslations_OrderedByKnownWord_FromSelectedDictionary(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation3 = Translation.objects.create(dictionary=dictionary,
                                                  known_word='TestKnown3',
                                                  word_to_learn='bbb')
        translation1 = Translation.objects.create(dictionary=dictionary,
                                                  known_word='TestKnown1',
                                                  word_to_learn='aaa')
        translation2 = Translation.objects.create(dictionary=dictionary,
                                                  known_word='TestKnown2',
                                                  word_to_learn='ccc')

        # When
        response = self.client.get(reverse('learn:translations', kwargs={'pk': dictionary.id}))

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['dictionary'].id,
                         dictionary.id)
        self.assertEqual(list(response.context['dictionary'].translation_set.all()),
                         [translation1,
                          translation2,
                          translation3])

    def test_shouldRedirect_ToDictionaries(self):
        # When
        response = self.client.get(reverse('learn:index'))

        # Then
        self.assertRedirects(response, reverse('learn:dictionaries'))
