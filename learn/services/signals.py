import smtplib

from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import get_template


def send_mail(subject, message, to):
    if not settings.LEARN_SMTP_ADDRESS or not settings.LEARN_SMTP_PASSWORD:
        return
    from_address = "%s <%s>" % ("Py3Learn", settings.LEARN_SMTP_ADDRESS)
    formatted_message = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" %
                         (from_address, ", ".join(to), subject)) + \
                        message + \
                        "\r\n"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(settings.LEARN_SMTP_ADDRESS, settings.LEARN_SMTP_PASSWORD)
    server.sendmail(from_address, to, formatted_message)
    server.quit()


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
         recipients)
