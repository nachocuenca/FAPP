
import os
from django.core.wsgi import get_wsgi_application

if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    raise RuntimeError('DJANGO_SETTINGS_MODULE no está configurado.')

application = get_wsgi_application()
