from django.core.urlresolvers import reverse
from django.test import TestCase


class LogoutTests(TestCase):
    def test_shouldRedirectUserToLogin(self):
        # When
        response = self.client.get(reverse('learn:logout'))

        # Then
        self.assertRedirects(response, reverse('learn:login'))
