from enum import Enum

LEARN_DUMMY = None
LEARN_RYTHM_MULTIPLIER = '2'
LEARN_BASE_RYTHM = '2'
LEARN_MAX_WORDS = '5'

available_settings = Enum('available_settings', 'LEARN_RYTHM_MULTIPLIER LEARN_BASE_RYTHM LEARN_MAX_WORDS')
