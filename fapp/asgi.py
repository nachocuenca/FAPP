"""
ASGI config for fapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    raise RuntimeError('DJANGO_SETTINGS_MODULE no está configurado.')

application = get_asgi_application()
