from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class SignupTests(TestCase):
    def test_shouldRouteToSignupPage(self):
        # When
        response = self.client.get(reverse('learn:signup'))

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("<h2>Sign up</h2>", response.content.decode('utf-8'))

    def test_shouldFindLinkInNavbar(self):
        # When
        response = self.client.get(reverse('learn:signup'))

        # Then
        self.assertInHTML("<li><a href=" + reverse('learn:signup') + ">Sign up</a></li>",
                          response.content.decode('utf-8'),
                          count=2)

    def test_shouldContainSignupForm(self):
        # When
        response = self.client.get(reverse('learn:signup'))

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
                            <input id="email" name="email" type="email" placeholder="you@example.com" value=""/>
                            <label for="email">Email</label>
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
                                Sign up
                                <i class="material-icons right">fingerprint</i>
                            </button>
                        </div>
                    </div>
                """, response.content.decode('utf-8'))

    def test_shouldSendFormData_ToSignIn(self):
        # When
        response = self.client.get(reverse('learn:signup'))

        # Then
        self.assertTrue('<form method="post" action="' + reverse('learn:signup') + '">'
                        in response.content.decode('utf8'))

    def test_shouldDisplayErrorText_WhenBadInput(self):
        # Given
        form_data = {
            'username': '',
            'email': '',
            'password': '',
        }

        # When
        response = self.client.post(reverse('learn:signup'), data=form_data)

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
                        Email:<br/>This field is required.<br/>
                    </div>
                """, response.content.decode('utf-8'))
        self.assertInHTML(
                """
                    <div class="card-panel red lighten-4">
                        Password:<br/>This field is required.<br/>
                    </div>
                """, response.content.decode('utf-8'))

    def test_shouldRedirectToDictionaries_WhenSuccessfulySignedIn(self):
        # Given
        form_data = {
            'username': 'someusername',
            'email': 'test@domain.com',
            'password': 'mysecurepassword',
        }

        # When
        response = self.client.post(reverse('learn:signup'), data=form_data)

        # Then
        self.assertRedirects(response, reverse('learn:dictionaries'))

    def test_shouldDisplayErrorText_WhenUsernameAlreadyExists(self):
        # Given
        User.objects.create_user(username='someusername',
                                 email='thing@dom.net',
                                 password='apassword')
        form_data = {
            'username': 'someusername',
            'email': 'test@domain.com',
            'password': 'mysecurepassword',
        }

        # When
        response = self.client.post(reverse('learn:signup'), data=form_data)

        # Then
        self.assertInHTML(
                """
                    <div class="card-panel red lighten-4">
                        Username:<br/>This username already exists.<br/>
                    </div>
                """, response.content.decode('utf-8'))

    def test_shouldRegisterAccountInDatabase_WhenSuccessfulySignedIn(self):
        form_data = {
            'username': 'someusername',
            'email': 'test@domain.com',
            'password': 'mysecurepassword',
        }

        # When
        self.client.post(reverse('learn:signup'), data=form_data)

        # Then
        self.assertTrue(User.objects.get(username='someusername'))

    def test_shouldBeMarkedAsActive_WhenSuccessfulySignedIn(self):
        # Given
        form_data = {
            'username': 'someusername',
            'email': 'some@email.com',
            'password': 'mysecurepassword',
        }

        # When
        response = self.client.post(reverse('learn:signup'), data=form_data)

        # Then
        user = User.objects.filter(username="someusername").first()
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)