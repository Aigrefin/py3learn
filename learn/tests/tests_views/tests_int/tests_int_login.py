from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class LoginTests(TestCase):
    def test_shouldRouteToLoginPage(self):
        # When
        response = self.client.get(reverse('learn:login'))

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("<h2>Log in</h2>", response.content.decode('utf-8'))

    def test_shouldFindLinkInNavbar(self):
        # When
        response = self.client.get(reverse('learn:login'))

        # Then
        self.assertInHTML("<li><a href=" + reverse('learn:login') + ">Log in</a></li>",
                          response.content.decode('utf-8'),
                          count=2)

    def test_shouldContainLoginForm(self):
        # When
        response = self.client.get(reverse('learn:login'))

        # Then
        self.assertInHTML(
                """
                    <div class="row">
                        <div class="col s12">
                            <input id="username" name="username" type="text" placeholder="user name" value=""/>
                            <label for="username">User name</label>
                        </div>
                    </div>
                """, response.content.decode('utf-8'))
        self.assertInHTML(
                """
                    <div class="row">
                        <div class="col s12">
                            <input id="password" name="password" type="password" class="validate">
                            <label for="password">Password</label>
                        </div>
                    </div>
                """, response.content.decode('utf-8'))
        self.assertInHTML(
                """
                    <div class="row">
                        <div class="col s12">
                            <button class="btn waves-effect waves-light" type="submit" name="action">
                                Log in
                                <i class="material-icons right">fingerprint</i>
                            </button>
                        </div>
                    </div>
                """, response.content.decode('utf-8'))

    def test_shouldSendFormData_ToLogIn(self):
        # When
        response = self.client.get(reverse('learn:login'))

        # Then
        self.assertTrue('<form method="post" action="' + reverse('learn:login') + '">'
                        in response.content.decode('utf8'))

    def test_shouldDisplayErrorText_WhenBadInput(self):
        # Given
        form_data = {
            'username': '',
            'password': '',
        }

        # When
        response = self.client.post(reverse('learn:login'), data=form_data)

        # Then
        self.assertInHTML(
                """
                    <div class="card-panel red lighten-4">
                        Username:<br/>This field is required.<br/>
                    </div>
                """, response.content.decode('utf-8'))
        self.assertInHTML(
                """
                    <div class="card-panel red lighten-4">
                        Password:<br/>This field is required.<br/>
                    </div>
                """, response.content.decode('utf-8'))

    def test_shouldRedirectToDictionaries_WhenSuccessfulyLoggedIn(self):
        # Given
        User.objects.create_user(username="someusername", password="mysecurepassword")
        form_data = {
            'username': 'someusername',
            'password': 'mysecurepassword',
        }

        # When
        response = self.client.post(reverse('learn:login'), data=form_data)

        # Then
        self.assertRedirects(response, reverse('learn:dictionaries'))

    def test_shouldDisplayErrorText_WhenBadUsernameIsGiven(self):
        # Given
        User.objects.create_user(username='someusername',
                                 password='mysecurepassword')
        form_data = {
            'username': 'badusername',
            'password': 'mysecurepassword',
        }

        # When
        response = self.client.post(reverse('learn:login'), data=form_data)

        # Then
        self.assertInHTML(
                """
                    <div class="card-panel red lighten-4">
                        Login failed:<br/>User name and/or password are incorrect.<br/>
                    </div>
                """, response.content.decode('utf-8'))

    def test_shouldDisplayErrorText_WhenBadPasswordIsGiven(self):
        # Given
        User.objects.create_user(username='someusername',
                                 password='mysecurepassword')
        form_data = {
            'username': 'someusername',
            'password': 'badpassword',
        }

        # When
        response = self.client.post(reverse('learn:login'), data=form_data)

        # Then
        self.assertInHTML(
                """
                    <div class="card-panel red lighten-4">
                        Login failed:<br/>User name and/or password are incorrect.<br/>
                    </div>
                """, response.content.decode('utf-8'))

    def test_shouldBeMarkedAsActive_WhenSuccessfulyLoggedIn(self):
        # Given
        user = User.objects.create_user(username="someusername", password="mysecurepassword")
        form_data = {
            'username': 'someusername',
            'password': 'mysecurepassword',
        }

        # When
        self.client.post(reverse('learn:login'), data=form_data)

        # Then
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)