import datetime
import math

import django

from learn.infrastructure.configuration import get_configuration

LEARN_RYTHM_MULTIPLIER = 'LEARN_RYTHM_MULTIPLIER'
LEARN_BASE_RYTHM = 'LEARN_BASE_RYTHM'


def compute_next_repetition(successes):
    next_repetition_delta = float(get_configuration(LEARN_BASE_RYTHM)) *\
                            math.pow(float(get_configuration(LEARN_RYTHM_MULTIPLIER)), successes)
    return django.utils.timezone.now() + datetime.timedelta(seconds=next_repetition_delta)
