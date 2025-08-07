from decimal import Decimal
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# --------------------------
# Usuario personalizado
# --------------------------
class Usuario(AbstractUser):
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

# --------------------------
# Cliente
# --------------------------

class Cliente(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    cif = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover - string representation
        return self.nombre



class Presupuesto(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    concepto = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:  # pragma: no cover - string representation
        return f"Presupuesto #{self.pk} - {self.cliente.nombre}"



# --------------------------
# Pedido
# --------------------------

class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    presupuesto = models.ForeignKey(
        Presupuesto, on_delete=models.SET_NULL, null=True, blank=True
    )

    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:  # pragma: no cover - string representation
        return f"Pedido #{self.pk} - {self.cliente.nombre}"


class Actuacion(models.Model):

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='actuaciones')
    fecha = models.DateField()
    descripcion = models.TextField()
    coste = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:  # pragma: no cover - string representation
        return f"Actuación #{self.pk} - {self.cliente.nombre}"


class Factura(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, null=True, blank=True)
    actuacion = models.ForeignKey(
        Actuacion, on_delete=models.SET_NULL, null=True, blank=True
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

    def save(self, *args, **kwargs) -> None:
        iva_amount = self.base_imponible * self.iva / Decimal("100")
        irpf_amount = self.base_imponible * self.irpf / Decimal("100")
        self.total = self.base_imponible + iva_amount - irpf_amount
        super().save(*args, **kwargs)

    def __str__(self) -> str:  # pragma: no cover - string representation
        return f"Factura {self.numero} - {self.cliente.nombre}"


