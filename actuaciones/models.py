from django.conf import settings
from django.db import models


class Actuacion(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="actuaciones",
    )
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    pedido = models.ForeignKey('pedidos.Pedido', on_delete=models.CASCADE, related_name='actuaciones')
    fecha = models.DateField()
    descripcion = models.TextField()
    coste = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"Actuación #{self.pk} - {self.cliente.nombre}"
