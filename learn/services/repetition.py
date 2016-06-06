import datetime
import math

import django
from py3njection import inject

from learn.infrastructure.configuration import LearnConfiguration
from learn.learn_base_settings import available_settings


@inject
def compute_next_repetition(successes, conf: LearnConfiguration):
    next_repetition_delta = float(conf.get_configuration(available_settings.LEARN_BASE_RYTHM)) * \
                            math.pow(float(conf.get_configuration(available_settings.LEARN_RYTHM_MULTIPLIER)),
                                     successes)
    return django.utils.timezone.now() + datetime.timedelta(seconds=next_repetition_delta)
