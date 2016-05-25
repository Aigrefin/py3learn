from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class BaseViewTests(TestCase):
    def test_shouldHideLoginAndSignin_AndHideLogout_WhenUserLoggedIn(self):
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
                '<li><a href="' + reverse('learn:signin') + '">Sign in</a></li>', response.content.decode('utf8'),
                count=0)
        self.assertInHTML(
                '<li><a href="' + reverse('learn:login') + '">Log in</a></li>', response.content.decode('utf8'),
                count=0)

    def test_shouldContainLinkToIssues(self):
        # When
        response = self.client.get(reverse('learn:dictionaries'))

        # Then
        self.assertInHTML(
                '<a class="grey-text text-lighten-4 right" href="https://github.com/Aigrefin/py3learn/issues" target="_blank">Issues ?</a>',
                response.content.decode('utf8')
        )
