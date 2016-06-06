from unittest import TestCase
from unittest.mock import MagicMock, create_autospec

from django.contrib.auth.models import User
from django.utils import timezone

from learn.infrastructure.database import Database
from learn.models import Dictionary, Translation, RythmNotation
from learn.services.choice import rythm_choice


def create_translations(numberOfTranslations, dictionary, user):
    translations = list()
    for currentTranslationNumber in range(0, numberOfTranslations):
        translation = Translation(dictionary=dictionary,
                                  known_word='TestKnown' + str(currentTranslationNumber),
                                  word_to_learn='TestLearn' + str(currentTranslationNumber))
        translations.append(translation)
        RythmNotation(user=user,
                      translation=translation,
                      successes=0,
                      next_repetition=timezone.now().replace(hour=currentTranslationNumber))

    return translations


class ChooseRythmNotationExerciseTests(TestCase):
    def setUp(self):
        self.conf = MagicMock()
        self.conf.get_configuration = MagicMock()
        self.database = MagicMock(spec=Database)
        self.database.get_ordered_scheduled_words_to_learn_before_date = MagicMock()
        self.database.plan_new_words_to_learn = MagicMock()
        self.user = User(username='a', password='b')
        self.dictionary = Dictionary(language='TestLang')

    def test_shouldReturnWord_FromDatabase(self):
        # Given
        translations = create_translations(1, self.dictionary, self.user)

        self.conf.get_configuration.return_value = 1
        self.database.get_ordered_scheduled_words_to_learn_before_date.return_value = translations

        # When
        result = rythm_choice(self.user, self.dictionary, database=self.database, conf=self.conf)

        # Then
        self.assertIn(result, translations)

    def test_shouldPrepareNeverSeenWords_ToCompleteCurrentWords_UpToMaxWordsToLearn(self):
        # Given
        translations = create_translations(2, self.dictionary, self.user)

        self.conf.get_configuration.return_value = 2
        self.database.get_ordered_scheduled_words_to_learn_before_date._mock_return_value = list()
        self.database.plan_new_words_to_learn.return_value = translations

        # When
        result = rythm_choice(self.user, self.dictionary, database=self.database, conf=self.conf)

        # Then
        self.assertIn(result, translations)
        words_to_complete_the_list = self.database.plan_new_words_to_learn.call_args_list[0][0][2]
        self.assertEqual(words_to_complete_the_list, 2)

    def test_shouldReturnNone_WhenNoWordForToday_AndNoNewWordCanBeAdded(self):
        # Given
        self.conf.get_configuration.return_value = 2
        self.database.get_ordered_scheduled_words_to_learn_before_date._mock_return_value = list()
        self.database.plan_new_words_to_learn.return_value = list()

        # When
        result = rythm_choice(self.user, self.dictionary, database=self.database, conf=self.conf)

        # Then
        self.assertIsNone(result)

    def test_shouldUseRandomChoice_ToReturnCurrentWord(self):
        # Given
        self.conf.get_configuration.return_value = 1
        translations = create_translations(1, self.dictionary, self.user)
        self.database.get_ordered_scheduled_words_to_learn_before_date.return_value = translations
        create_autospec("learn.services.choice.random.choice", translations[0])

        # When
        result = rythm_choice(self.user, self.dictionary, database=self.database, conf=self.conf)

        # Then
        self.assertEqual(result, translations[0])
