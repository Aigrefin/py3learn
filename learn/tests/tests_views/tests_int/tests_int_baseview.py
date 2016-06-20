from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class BaseViewTests(TestCase):
    def test_shouldHideLoginAndSignup_AndHideLogout_WhenUserLoggedIn(self):
        # Given
        user = User.objects.create_user(username="someusername", password="mysecurepassword")
        form_data = {
            'username': 'someusername',
            'password': 'mysecurepassword',
        }
        self.client.post(reverse('learn:login'), data=form_data)

        # When
        response = self.client.get(reverse('learn:dictionaries'))

        # Then
        self.assertInHTML(
                '<li><a href="' + reverse('learn:logout') + '">Log out</a></li>', response.content.decode('utf8'),
                count=2)
        self.assertInHTML(
                '<li><a href="' + reverse('learn:signup') + '">Sign up</a></li>', response.content.decode('utf8'),
                count=0)
        self.assertInHTML(
                '<li><a href="' + reverse('learn:login') + '">Log in</a></li>', response.content.decode('utf8'),
                count=0)
