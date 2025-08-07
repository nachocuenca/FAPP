"""Configuración de tests.

Esta configuración reutiliza todas las opciones del módulo ``settings`` pero
fuerza el uso de una base de datos SQLite en memoria para que los tests se
puedan ejecutar sin depender de variables de entorno.
"""

import os


# Fuerza el uso de SQLite en ``settings`` antes de importar cualquier ajuste.
os.environ.setdefault("USE_SQLITE", "1")

from .settings import *  # noqa: F403,F401

# Base de datos en memoria para los tests.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Evita ejecutar migraciones durante los tests para acelerar la suite.
MIGRATION_MODULES = {
    "core": None,
    "clientes": None,
    "presupuestos": None,
}

# Configuración de seguridad relajada para evitar redirecciones HTTPS en tests.
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
