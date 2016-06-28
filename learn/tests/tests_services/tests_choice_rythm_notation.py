import random
from unittest import TestCase
from unittest.mock import MagicMock, create_autospec, patch

from django.contrib.auth.models import User
from django.utils import timezone

from learn.infrastructure.configuration import LearnConfiguration
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
        self.conf = MagicMock(spec=LearnConfiguration)
        self.database = MagicMock(spec=Database)
        self.user = User(username='a', password='b')
        self.dictionary = Dictionary(language='TestLang')

    def test_shouldReturnWord_FromDatabase(self):
        # Given
        translations = create_translations(1, self.dictionary, self.user)

        self.conf.get_configuration.return_value = 1
        self.database.get_ordered_scheduled_words_to_learn_before_date.return_value = translations

        # When
        result = rythm_choice(self.user, self.dictionary, database=self.database, conf=self.conf,
                              rand=MagicMock(random))

        # Then
        self.assertIn(result, translations)

    def test_shouldPrepareNeverSeenWords_ToCompleteCurrentWords_UpToMaxWordsToLearn(self):
        # Given
        translations = create_translations(2, self.dictionary, self.user)

        self.conf.get_configuration.return_value = 2
        self.database.get_ordered_scheduled_words_to_learn_before_date._mock_return_value = list()
        self.database.get_unseen_words._mock_return_value = translations

        # When
        result = rythm_choice(self.user, self.dictionary, database=self.database, conf=self.conf,
                              rand=MagicMock(random))

        # Then
        self.assertIn(result, translations)
        words_to_complete_the_list = self.database.get_unseen_words.call_args_list[0][0][1]
        self.assertEqual(words_to_complete_the_list, 2)
        self.assertEqual(self.database.schedule_words.call_args_list[0][0][0], translations)

    def test_shouldReturnNone_WhenNoWordForToday_AndNoNewWordCanBeAdded(self):
        # Given
        self.conf.get_configuration.return_value = 2
        self.database.get_ordered_scheduled_words_to_learn_before_date._mock_return_value = list()
        self.database.get_unseen_words._mock_return_value = list()

        # When
        result = rythm_choice(self.user, self.dictionary, database=self.database, conf=self.conf,
                              rand=MagicMock(random))

        # Then
        self.assertIsNone(result)

    def test_shouldUseRandomChoice_ToReturnCurrentWord(self):
        # Given
        self.conf.get_configuration.return_value = 1
        translations = create_translations(1, self.dictionary, self.user)
        self.database.get_ordered_scheduled_words_to_learn_before_date.return_value = translations
        create_autospec("learn.services.choice.random.choice", translations[0])

        # When
        result = rythm_choice(self.user, self.dictionary, database=self.database, conf=self.conf,
                              rand=MagicMock(random))

        # Then
        self.assertEqual(result, translations[0])

    def test_shouldGiveARandomChanceOf_OneOnAHundred(self):
        # Given
        random_mock = MagicMock(random)

        # When
        rythm_choice(self.user, self.dictionary, database=self.database, conf=self.conf,
                     rand=random_mock)

        # Then
        random_mock.randint.assert_called_with(1, 100)

    def test_shouldReturnWellKnownWordWhenHasTheChance(self):
        # Given
        random_mock = MagicMock(random)
        random_mock.randint.return_value = 1
        translations = create_translations(1, self.dictionary, self.user)
        self.database.get_random_well_known_word.return_value = translations[0]

        # When
        result = rythm_choice(self.user, self.dictionary, database=self.database, conf=self.conf,
                              rand=random_mock)

        # Then
        self.assertEqual(result, translations[0])

    @patch("learn.services.choice.timezone.now")
    def test_shouldContinueChoice_WhenNoWellKnownWordAvailable(self, time_mock):
        # Given
        random_mock = MagicMock(random)
        random_mock.randint.return_value = 1
        self.database.get_random_well_known_word.return_value = None

        # When
        rythm_choice(self.user, self.dictionary, database=self.database, conf=self.conf,
                     rand=random_mock)

        # Then
        self.database.get_ordered_scheduled_words_to_learn_before_date \
            .assert_called_once_with(time_mock.return_value, self.user, self.dictionary)
