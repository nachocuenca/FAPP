from decimal import Decimal
from django.conf import settings
from django.db import models


class Factura(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="facturas",
    )
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    pedido = models.ForeignKey('pedidos.Pedido', on_delete=models.SET_NULL, null=True, blank=True)
    actuacion = models.ForeignKey(
        'actuaciones.Actuacion', on_delete=models.SET_NULL, null=True, blank=True
    )
    fecha = models.DateField()
    numero = models.CharField(max_length=20, unique=True)
    base_imponible = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=21.00)
    irpf = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("borrador", "Borrador"),
            ("enviado", "Enviado"),
            ("pagado", "Pagado"),
        ],
        default="borrador",
    )

    class Meta:
        indexes = [models.Index(fields=["usuario"])]

    def save(self, *args, **kwargs) -> None:
        iva_amount = self.base_imponible * self.iva / Decimal("100")
        irpf_amount = self.base_imponible * self.irpf / Decimal("100")
        self.total = self.base_imponible + iva_amount - irpf_amount
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Factura {self.numero} - {self.cliente.nombre}"
