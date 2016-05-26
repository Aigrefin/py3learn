import datetime
import math

import django

SUCCESS_MULTIPLIER = 2
BASE_SECONDS = 2


def compute_next_repetition(successes):
    next_repetition_delta = BASE_SECONDS * math.pow(SUCCESS_MULTIPLIER, successes)
    return django.utils.timezone.now() + datetime.timedelta(seconds=next_repetition_delta)
