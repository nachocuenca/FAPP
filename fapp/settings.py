from pathlib import Path
import os
import importlib

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def get_env(name, default=None, required=False):
    """Obtiene una variable de entorno o lanza un error descriptivo."""
    value = os.environ.get(name, default)
    if required and value is None:
        raise ImproperlyConfigured(
            f"Falta la variable de entorno {name} para la configuración.")
    return value

# En producción este valor debe definirse mediante la variable de entorno
# SECRET_KEY. El valor por defecto sólo debe usarse durante el desarrollo.
SECRET_KEY = os.environ.get("SECRET_KEY", "definir-en-produccion")

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1")

ALLOWED_HOSTS = (
    os.environ.get("ALLOWED_HOSTS", "").split(",")
    if os.environ.get("ALLOWED_HOSTS")
    else []
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'adminlte3',
    'adminlte3_theme',
    'django_bootstrap5',
    'core',
    'clientes',
    'presupuestos',
    'plantillas',
    'configuracion',
    'pedidos',
    'actuaciones',
    'facturas',
    'usuarios',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fapp.wsgi.application'

if os.environ.get("USE_SQLITE") == "1":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    try:
        importlib.import_module("psycopg2")
    except Exception as exc:
        raise ImproperlyConfigured(
            "La librería 'psycopg2-binary' es necesaria para PostgreSQL. "
            "Instálala con 'pip install psycopg2-binary'."
        ) from exc

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

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'usuarios.Usuario'

SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "True").lower() in ("true", "1")
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "True").lower() in ("true", "1")
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "True").lower() in ("true", "1")
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", "True").lower() in ("true", "1")
SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "True").lower() in ("true", "1")
