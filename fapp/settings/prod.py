from .base import *  # noqa

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env('POSTGRES_DB', required=True),
        'USER': get_env('POSTGRES_USER', required=True),
        'PASSWORD': get_env('POSTGRES_PASSWORD', required=True),
        'HOST': get_env('POSTGRES_HOST', required=True),
        'PORT': get_env('POSTGRES_PORT', required=True),
    }
}
