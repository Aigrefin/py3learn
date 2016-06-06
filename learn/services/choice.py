import random
from itertools import chain

from django.utils import timezone
from py3njection import inject

from learn.infrastructure.configuration import LearnConfiguration
from learn.infrastructure.database import Database
from learn.learn_base_settings import available_settings
from learn.models import Translation


def random_choice(dictionary_pk):
    translation = Translation.objects.filter(dictionary__id=dictionary_pk).order_by('?').first()
    return translation


@inject
def rythm_choice(dictionary_pk, user, database: Database, conf: LearnConfiguration):
    choose_before = timezone.now()
    words = database.get_ordered_scheduled_words_to_learn_before_date(choose_before, dictionary_pk, user)
    max_words = get_max_words(conf)
    need_more_words = len(words) < max_words
    if need_more_words:
        words = prepare_more_words(database, dictionary_pk, max_words, user, words)
    return choose_word(max_words, words)


def get_max_words(conf):
    max_words_configuration = conf.get_configuration(available_settings.LEARN_MAX_WORDS)
    return int(max_words_configuration)


def prepare_more_words(database, dictionary_pk, max_words, user, words):
    quantity_of_words_to_plan = (max_words - len(words))
    translations = database.plan_new_words_to_learn(dictionary_pk, user, quantity_of_words_to_plan)
    words = list(chain(words, translations))
    return words


def choose_word(max_words, words):
    if words:
        max_learnable_words = words[:min(max_words, len(words))]
        return random.choice(max_learnable_words)
    return None
