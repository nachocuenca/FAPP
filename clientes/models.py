from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Cliente(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clientes",
    )
    nombre = models.CharField(max_length=100)
    cif = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^[A-Z0-9]{1,20}$', 'CIF inválido')],
    )
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["usuario"])]
        constraints = [
            models.UniqueConstraint(
                fields=['cif'],
                condition=~models.Q(cif__isnull=True) & ~models.Q(cif=''),
                name='unique_cif_nonblank'
            )
        ]

    def __str__(self) -> str:
        return self.nombre
