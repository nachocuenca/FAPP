import importlib

from django.apps import AppConfig
from django.db import connections
from django.db.utils import OperationalError


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        self._check_external_libs()
        self._check_database_connection()

    def _check_external_libs(self):
        for lib in ("xhtml2pdf", "reportlab"):
            try:
                importlib.import_module(lib)
            except ImportError as exc:
                raise RuntimeError(
                    f"No se pudo importar la librería externa '{lib}'. "
                    "Instálala en el entorno antes de continuar."
                ) from exc

    def _check_database_connection(self):
        db_conn = connections["default"]
        try:
            db_conn.cursor()
        except OperationalError as exc:
            raise RuntimeError(
                "No se pudo conectar a la base de datos. Revisa la "
                "configuración y que el servidor esté disponible."
            ) from exc
