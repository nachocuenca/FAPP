from django.contrib import admin
from .models import Factura


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ["numero", "cliente", "fecha", "total", "estado"]
    search_fields = ["numero", "cliente__nombre"]
    list_filter = ["fecha", "estado", "cliente"]
