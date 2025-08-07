
from django.contrib import admin
from .models import Usuario, Cliente, Presupuesto, Pedido

admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Presupuesto)
admin.site.register(Pedido)
