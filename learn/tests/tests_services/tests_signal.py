from unittest.mock import Mock, MagicMock

from django.contrib.auth.models import User
from django.test import TestCase

from learn.models import Translation, Dictionary
from learn.services import signals


class SignalsTests(TestCase):
    def test_shouldSendMailContaining_DictionaryLanguage_KnownWord_WordToLearn(self):
        # Given
        false_send_mail = Mock()

        false_objects = MagicMock()
        false_objects.filter.return_value = [User(email='test@test.com',is_staff=False,is_superuser=False)]
        false_users_db = MagicMock()
        false_users_db.objects = false_objects

        dictionary = Dictionary(language='Vietnamese')
        translation = Translation(known_word='Bien mangé, plein', word_to_learn='No', dictionary=dictionary)

        # When
        signals.send_mail_on_new_word(Translation, instance=translation, send=false_send_mail,
                                      user_objects=false_users_db)

        # Then
        args_list = false_send_mail.call_args_list[0][0]
        self.assertEqual(args_list[0], 'New word : Bien mangé, plein')
        self.assertEqual(args_list[1], 'Hi !\n\n'
                                       'A new word has been added to the Vietnamese dictionary.\n\n'
                                       'Known word : Bien mangé, plein'
                                       '\nWord to learn : No\n\n'
                                       'Seen you soon !')
        self.assertEqual(args_list[2], ['test@test.com'])
