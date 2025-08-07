from django.contrib import admin
from .models import Usuario, Cliente, Pedido, Actuacion, Factura

admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Actuacion)
admin.site.register(Factura)
