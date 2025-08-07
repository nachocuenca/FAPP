"""Admin configuration for core models."""

from django.contrib import admin

from .models import Actuacion, Cliente, Factura, Pedido, Presupuesto, Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """Admin options for :class:`Usuario`."""

    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "telefono",
        "is_staff",
    ]
    search_fields = ["username", "email", "first_name", "last_name"]
    list_filter = ["is_staff", "is_superuser", "is_active"]


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Admin options for :class:`Cliente`."""

    list_display = ["nombre", "cif", "email", "telefono", "activo"]
    search_fields = ["nombre", "cif", "email"]
    list_filter = ["activo"]


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    """Admin options for :class:`Presupuesto`."""

    list_display = ["cliente", "fecha", "concepto", "total"]
    search_fields = ["cliente__nombre", "concepto"]
    list_filter = ["fecha", "cliente"]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """Admin options for :class:`Pedido`."""

    list_display = ["cliente", "fecha", "descripcion", "total"]
    search_fields = ["cliente__nombre", "descripcion"]
    list_filter = ["fecha", "cliente"]


@admin.register(Actuacion)
class ActuacionAdmin(admin.ModelAdmin):
    """Admin options for :class:`Actuacion`."""

    list_display = ["cliente", "pedido", "fecha", "coste"]
    search_fields = ["cliente__nombre", "pedido__descripcion", "descripcion"]
    list_filter = ["fecha", "cliente"]


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    """Admin options for :class:`Factura`."""

    list_display = ["numero", "cliente", "fecha", "total", "estado"]
    search_fields = ["numero", "cliente__nombre"]
    list_filter = ["fecha", "estado", "cliente"]

