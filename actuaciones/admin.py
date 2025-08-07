from django.contrib import admin
from .models import Actuacion


@admin.register(Actuacion)
class ActuacionAdmin(admin.ModelAdmin):
    list_display = ["cliente", "pedido", "fecha", "coste"]
    search_fields = ["cliente__nombre", "pedido__descripcion", "descripcion"]
    list_filter = ["fecha", "cliente"]
