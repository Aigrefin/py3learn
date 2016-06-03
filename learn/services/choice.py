import random
from itertools import chain

from django.db.models import Q
from django.utils import timezone

from learn.infrastructure.configuration import get_configuration
from learn.learn_base_settings import available_settings
from learn.models import Translation, RythmNotation


def random_choice(dictionary_pk):
    translation = Translation.objects.filter(dictionary__id=dictionary_pk).order_by('?').first()
    return translation


def rythm_choice(user, dictionary_pk):
    choose_before = timezone.now()
    word_of_the_day = get_next_word(dictionary_pk, choose_before, user)
    if not word_of_the_day:
        new_batch_of_translations = prepare_next_batch(dictionary_pk, user)
        if new_batch_of_translations:
            word_of_the_day = new_batch_of_translations[0]
    return word_of_the_day


def get_next_word(dictionary_pk, choose_before, user):
    words = Translation.objects \
        .filter(dictionary_id=dictionary_pk, rythmnotation__user=user, rythmnotation__next_repetition__lt=choose_before) \
        .order_by('rythmnotation__next_repetition')
    max_words = int(get_configuration(available_settings.LEARN_MAX_WORDS))
    if len(words) < max_words:
        translations = Translation.objects.filter(
                Q(dictionary_id=dictionary_pk),
                ~Q(rythmnotation__user=user))[:(max_words - len(words))]
        for translation in translations:
            RythmNotation.objects.create(user=user, translation=translation, successes=0,
                                         next_repetition=timezone.now())
        words = list(chain(words, translations))
    if words:
        return random.choice(words)
    else:
        return None


def prepare_next_batch(dictionary_pk, user):
    max_words = int(get_configuration(available_settings.LEARN_MAX_WORDS))
    new_batch_of_translations = Translation.objects.filter(
            Q(dictionary_id=dictionary_pk),
            ~Q(rythmnotation__user=user))[:max_words]
    for translation in new_batch_of_translations:
        RythmNotation.objects.create(user=user, translation=translation, successes=0,
                                     next_repetition=timezone.now())
    return new_batch_of_translations
