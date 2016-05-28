from unittest.mock import MagicMock

from django.test import TestCase

from learn.infrastructure.configuration import get_configuration, set_configuration
from learn.models import Configuration


class ConfigurationTests(TestCase):
    def setUp(self):
        self.configuration_objects = MagicMock()
        self.configuration_model = MagicMock()
        self.configuration_model.objects = self.configuration_objects

    def test_shouldReturnConfigurationAtSpecifiedKey(self):
        # Given
        self.configuration_objects.filter.return_value = [Configuration(key='A_KEY', value='AValue'), ]

        # When
        result = get_configuration('A_KEY', configuration_model=self.configuration_model)

        # Then
        self.assertEqual(result, 'AValue')

    def test_shouldReturnNoneWhenNoConfigurationExists(self):
        # Given
        self.configuration_objects.filter.return_value = []

        # When
        try:
            get_configuration('NONE', configuration_model=self.configuration_model)

        # Then
        except AttributeError as e:
            self.assertEqual("'Settings' object has no attribute 'NONE'", str(e))

    def test_shouldReturnDefaultMaxWordsLearningFromSettingsWhenNoEntryExists(self):
        for given_key, expected_value in {
            'LEARN_RYTHM_MULTIPLIER': '2',
            'LEARN_BASE_RYTHM': '2',
            'LEARN_MAX_WORDS': '5',
        }.items():
            # Given
            self.configuration_objects.filter.return_value = []

            # When
            result = get_configuration(given_key, configuration_model=self.configuration_model)

            # Then
            self.assertEqual(result, expected_value)

    def test_shouldRecordGivenConfiguration(self):
        # Given
        self.configuration_objects.create = MagicMock()

        # When
        set_configuration('SOME_KEY', 'SOME_VALUE', configuration_model=self.configuration_model)

        # Then
        kwargs = self.configuration_objects.create.call_args_list[0][1]
        self.assertEqual(kwargs['key'], 'SOME_KEY')
        self.assertEqual(kwargs['value'], 'SOME_VALUE')
