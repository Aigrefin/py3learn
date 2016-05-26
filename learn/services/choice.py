from django.db.models import Q
from django.utils import timezone

from learn.models import Translation, RythmNotation


def random_choice(dictionary_pk):
    translation = Translation.objects.filter(dictionary__id=dictionary_pk).order_by('?').first()
    return translation


def rythm_choice(user, dictionary_pk):
    tomorrow = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timezone.timedelta(days=1)
    word_of_the_day = get_next_word(dictionary_pk, tomorrow, user)
    if not word_of_the_day:
        new_batch_of_translations = prepare_next_batch(dictionary_pk, user, word_of_the_day)
        if new_batch_of_translations:
            word_of_the_day = new_batch_of_translations[0]
    return word_of_the_day


def get_next_word(dictionary_pk, tomorrow, user):
    word_of_the_day = Translation.objects \
        .filter(dictionary_id=dictionary_pk, rythmnotation__user=user, rythmnotation__next_repetition__lt=tomorrow) \
        .order_by('rythmnotation__next_repetition') \
        .first()
    return word_of_the_day


def prepare_next_batch(dictionary_pk, user, word_of_the_day):
    new_batch_of_translations = Translation.objects.filter(
            Q(dictionary_id=dictionary_pk),
            ~Q(rythmnotation__user=user)) \
        .order_by('rythmnotation__next_repetition')[:5]
    for translation in new_batch_of_translations:
        RythmNotation.objects.create(user=user, translation=translation, successes=0,
                                     next_repetition=timezone.now())
    return new_batch_of_translations
