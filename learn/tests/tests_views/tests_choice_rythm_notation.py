from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from learn.models import Dictionary, Translation, RythmNotation
from learn.services.choice import rythm_choice


def createTranslations(dictionary, number, user):
    translations = []
    for i in range(number):
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown' + str(i),
                                                 word_to_learn='TestLearn' + str(i))
        translations.append(translation)
        RythmNotation.objects.create(user=user,
                                     translation=translation,
                                     successes=0,
                                     next_repetition=timezone.now().replace(hour=i))
    return translations


class ChooseRythmNotationExerciseTests(TestCase):
    def test_shouldReturnFirstWord_WithRepetitionForToday(self):
        # Given
        user = User.objects.create_user(username='a', password='b')
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = createTranslations(dictionary, 6, user)[0]

        # When
        result = rythm_choice(user, dictionary)
        # Then
        self.assertEqual(result.rythmnotation_set.filter(user=user).first().next_repetition.day, timezone.now().day)

    def test_shouldPrepareBatchOfNeverSeenWords_BeforeReturningFirstWord_WithRepetitionForToday(self):
        # Given
        user = User.objects.create_user(username='a', password='b')
        dictionary = Dictionary.objects.create(language='TestLang')
        translation1 = Translation.objects.create(dictionary=dictionary,
                                                  known_word='TestKnown1',
                                                  word_to_learn='TestLearn1')
        translation2 = Translation.objects.create(dictionary=dictionary,
                                   known_word='TestKnown2',
                                   word_to_learn='TestLearn2')

        # When
        result = rythm_choice(user, dictionary)

        # Then
        self.assertTrue(result == translation1 or result == translation2)


    def test_shouldReturnNone_WhenNoWordForToday_AndNoNewWordCanBeAdded(self):
        # Given
        user = User.objects.create_user(username='a', password='b')
        dictionary = Dictionary.objects.create(language='TestLang')

        # When
        result = rythm_choice(user, dictionary)

        # Then
        self.assertEqual(None, result)

    def test_shouldReturnOneTranslation_FromASet(self):
        # Given
        dictionary = Dictionary.objects.create(language='TestLang')
        translation = Translation.objects.create(dictionary=dictionary,
                                                 known_word='TestKnown3',
                                                 word_to_learn='TestLearn3')

        url_parameters = {'dictionary_pk': dictionary.id}

        # When
        response = self.client.get(reverse('learn:choose_exercise', kwargs=url_parameters))

        # Then
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('learn:exercise', kwargs={
            'dictionary_pk': dictionary.id,
            'translation_pk': translation.id
        }))