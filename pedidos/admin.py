from django.contrib import admin
from .models import Pedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["cliente", "fecha", "descripcion", "total"]
    search_fields = ["cliente__nombre", "descripcion"]
    list_filter = ["fecha", "cliente"]
