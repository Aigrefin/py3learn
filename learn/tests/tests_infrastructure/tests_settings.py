from unittest import TestCase

from learn import learn_base_settings


class SettingsTests(TestCase):
    def test_shouldProveThatEnumHasADjangoSettingEquivalent(self):
        for enum in list(learn_base_settings.available_settings):
            # When
            try:
                getattr(learn_base_settings, enum.name)
            # Then
            except:
                self.fail('Expected enum to exists as Django settings : '+enum.name)
