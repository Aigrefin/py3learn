from django.conf import settings

from learn.models import Configuration


def get_configuration(key, configuration_model=Configuration):
    configuration = configuration_model.objects.filter(key=key)
    if configuration:
        return configuration[0].value
    return settings.__getattr__(key)


def set_configuration(key, value, configuration_model=Configuration):
    configuration_model.objects.create(key=key, value=value)
