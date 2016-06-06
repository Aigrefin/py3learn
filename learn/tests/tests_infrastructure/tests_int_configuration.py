from enum import Enum
from unittest.mock import MagicMock

from django.test import TestCase

from learn.infrastructure.configuration import LearnConfiguration
from learn.models import Configuration


class ConfigurationIntTests(TestCase):
    def setUp(self):
        self.configuration_objects = MagicMock()
        self.configuration_model = MagicMock()
        self.configuration_model.objects = self.configuration_objects
        self.conf = LearnConfiguration()

    def test_shouldReturnConfigurationAtSpecifiedKey(self):
        # Given
        enum = Enum('enum', 'A_KEY')
        self.configuration_objects.filter.return_value = [Configuration(key='A_KEY', value='AValue'), ]

        # When
        result = self.conf.get_configuration(enum.A_KEY, configuration_model=self.configuration_model)

        # Then
        self.assertEqual(result, 'AValue')

    def test_shouldReturnNoneWhenNoConfigurationExists(self):
        # Given
        enum = Enum('enum', 'NONE')
        self.configuration_objects.filter.return_value = []

        # When
        try:
            self.conf.get_configuration(enum.NONE, configuration_model=self.configuration_model)

        # Then
        except AttributeError as e:
            self.assertEqual("'Settings' object has no attribute 'NONE'", str(e))

    def test_shouldReturnDefaultMaxWordsLearningFromSettingsWhenNoEntryExists(self):
        enum = Enum('enum', 'LEARN_RYTHM_MULTIPLIER LEARN_BASE_RYTHM LEARN_MAX_WORDS')
        for given_key, expected_value in {
            'LEARN_RYTHM_MULTIPLIER': '2',
            'LEARN_BASE_RYTHM': '2',
            'LEARN_MAX_WORDS': '5',
        }.items():
            # Given
            self.configuration_objects.filter.return_value = []

            # When
            result = self.conf.get_configuration(enum.__getattr__(given_key),
                                                 configuration_model=self.configuration_model)

            # Then
            self.assertEqual(result, expected_value)

    def test_shouldRecordGivenConfiguration(self):
        # Given
        self.configuration_objects.create = MagicMock()

        # When
        self.conf.set_configuration('SOME_KEY', 'SOME_VALUE', configuration_model=self.configuration_model)

        # Then
        kwargs = self.configuration_objects.create.call_args_list[0][1]
        self.assertEqual(kwargs['key'], 'SOME_KEY')
        self.assertEqual(kwargs['value'], 'SOME_VALUE')
