from django.contrib import admin
from .models import Presupuesto


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ["cliente", "fecha", "concepto", "total"]
    search_fields = ["cliente__nombre", "concepto"]
    list_filter = ["fecha", "cliente"]
