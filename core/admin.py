from django.contrib import admin
from .models import Usuario, Cliente, Presupuesto, Pedido, Actuacion, Factura

admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Presupuesto)
admin.site.register(Pedido)
admin.site.register(Actuacion)
admin.site.register(Factura)
