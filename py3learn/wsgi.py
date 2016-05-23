"""
WSGI config for py3learn project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.cache.backends.memcached import BaseMemcachedCache
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

BaseMemcachedCache.close = lambda self, **kwargs: None
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "py3learn.prod_settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
