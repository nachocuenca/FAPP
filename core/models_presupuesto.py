
from django.db import models
from core.models import Cliente

class Presupuesto(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]
    fecha = models.DateField(auto_now_add=True)
    numero = models.CharField(max_length=20)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    concepto = models.TextField(blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"{self.numero} - {self.cliente.nombre}"
