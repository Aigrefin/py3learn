from unittest import TestCase

from learn.infrastructure.strings import caseless_equal


class StringsTests(TestCase):
    def test_shouldReturnEqual_OnExactlyTheSameString(self):
        # Given
        string = "some text"

        # When
        result = caseless_equal(string, string)

        # Then
        self.assertTrue(result)

    def test_shouldReturnNotEqual_OnStrictlyDifferentStrings(self):
        # Given
        string = "some text"
        differentString = "different text"

        # When
        result = caseless_equal(string, differentString)

        # Then
        self.assertFalse(result)

    def test_shouldReturnEqual_OnStringsOfDifferentCases(self):
        # Given
        string = "sOmE text"
        differentCaseString = "SoMe TeXt"

        # When
        result = caseless_equal(string, differentCaseString)

        # Then
        self.assertTrue(result)

    def test_shouldReturnEqual_OnStringsOfDifferentCases_AndForeignSpecialLetters(self):
        # Given
        string = "BẦu Straße"
        differentCaseString = "bầu strasse"

        # When
        result = caseless_equal(string, differentCaseString)

        # Then
        self.assertTrue(result)
