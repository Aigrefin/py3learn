import os

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template

from py3learn import prod_settings


def send_mail_on_new_word(sender, send=send_mail, user_objects=User, **kwargs):
    users = list(user_objects.objects.all())
    recipients = list([user.email for user in users])
    translation = kwargs['instance']
    send('New word : ' + str(translation.known_word),
         get_template("learn/new_word_email.html").render(context={
             'language': str(translation.dictionary.language),
             'known_word': str(translation.known_word),
             'word_to_learn': str(translation.word_to_learn)
         }),
         "learn@"+os.environ['MAILGUN_DOMAIN'],
         recipients, fail_silently=False)
