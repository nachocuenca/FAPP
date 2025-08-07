
import os
from django.core.asgi import get_asgi_application

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    raise RuntimeError('DJANGO_SETTINGS_MODULE no está configurado.')

application = get_asgi_application()
