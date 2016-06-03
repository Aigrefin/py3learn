from enum import Enum

from django.conf import settings

from learn.models import Configuration


def get_configuration(key: Enum, configuration_model=Configuration):
    configuration = configuration_model.objects.filter(key=key.name)
    if configuration:
        return configuration[0].value
    return settings.__getattr__(key.name)


def set_configuration(key, value, configuration_model=Configuration):
    configuration_model.objects.create(key=key, value=value)
