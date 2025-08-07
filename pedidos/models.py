from django.conf import settings
from django.db import models


class Pedido(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pedidos",
    )
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    presupuesto = models.ForeignKey(
        'presupuestos.Presupuesto', on_delete=models.SET_NULL, null=True, blank=True
    )
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [models.Index(fields=["usuario"])]

    def __str__(self) -> str:
        return f"Pedido #{self.pk} - {self.cliente.nombre}"
