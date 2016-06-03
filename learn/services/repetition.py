import datetime
import math

import django

from learn.infrastructure.configuration import get_configuration
from learn.learn_base_settings import available_settings


def compute_next_repetition(successes):
    next_repetition_delta = float(get_configuration(available_settings.LEARN_BASE_RYTHM)) * \
                            math.pow(float(get_configuration(available_settings.LEARN_RYTHM_MULTIPLIER)),
                                     successes)
    return django.utils.timezone.now() + datetime.timedelta(seconds=next_repetition_delta)
