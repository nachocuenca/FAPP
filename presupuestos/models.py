from django.conf import settings
from django.db import models


class Presupuesto(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="presupuestos",
    )
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    fecha = models.DateField()
    concepto = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"Presupuesto #{self.pk} - {self.cliente.nombre}"
