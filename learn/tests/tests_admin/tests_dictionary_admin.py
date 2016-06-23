from unittest import TestCase
from unittest.mock import MagicMock

from learn.admin import DictionaryAdmin
from learn.models import Translation
from learn.services.normalizer import TranslationNormalizer


class DictionaryAdminTests(TestCase):
    def test_thatShouldSaveFormset(self):
        # Given
        dictionary_admin = DictionaryAdmin(MagicMock(), MagicMock())
        formset_mock = MagicMock()

        # When
        dictionary_admin.save_formset(MagicMock(), MagicMock(),
                                      formset_mock,
                                      MagicMock(), normalizer=MagicMock())

        # Then
        formset_mock.save.assert_called_once_with(commit=False)

    def test_thatShouldDeleteFormsetObjects(self):
        # Given
        dictionary_admin = DictionaryAdmin(MagicMock(), MagicMock())
        translation_mock = MagicMock(Translation)
        formset_mock = MagicMock()
        formset_mock.deleted_objects = [translation_mock]

        # When
        dictionary_admin.save_formset(MagicMock(), MagicMock(),
                                      formset_mock,
                                      MagicMock(), normalizer=MagicMock())

        # Then
        translation_mock.delete.assert_called_once_with()

    def test_thatShouldNormalizeFormsetObjects(self):
        # Given
        dictionary_admin = DictionaryAdmin(MagicMock(), MagicMock())
        translation_mock = MagicMock(Translation)
        formset_mock = MagicMock()
        formset_mock.save.return_value = [translation_mock]
        normalizer = MagicMock(TranslationNormalizer)

        # When
        dictionary_admin.save_formset(MagicMock(), MagicMock(),
                                      formset_mock,
                                      MagicMock(), normalizer=normalizer)

        # Then
        normalizer.normalize_translation.assert_called_once_with(translation_mock)

    def test_thatShouldSaveNormalizedFormsetObjects(self):
        # Given
        dictionary_admin = DictionaryAdmin(MagicMock(), MagicMock())
        translation_mock = MagicMock(Translation)
        normalized_translation_mock = MagicMock(Translation)
        formset_mock = MagicMock()
        formset_mock.save.return_value = [translation_mock]
        normalizer = MagicMock(TranslationNormalizer)
        normalizer.normalize_translation.return_value = normalized_translation_mock

        # When
        dictionary_admin.save_formset(MagicMock(), MagicMock(),
                                      formset_mock,
                                      MagicMock(), normalizer=normalizer)

        # Then
        normalized_translation_mock.save.assert_called_once_with()

    def test_thatShouldSaveM2M(self):
        # Given
        dictionary_admin = DictionaryAdmin(MagicMock(), MagicMock())
        formset_mock = MagicMock()

        # When
        dictionary_admin.save_formset(MagicMock(), MagicMock(),
                                      formset_mock,
                                      MagicMock(), normalizer=MagicMock())

        # Then
        formset_mock.save_m2m.assert_called_once_with()
