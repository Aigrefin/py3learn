from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


def create_and_login_a_user(client):
    user = User.objects.create_user(username="someusername", password="mysecurepassword")
    form_data = {
        'username': 'someusername',
        'password': 'mysecurepassword',
    }
    client.post(reverse('learn:login'), data=form_data)
    return user
