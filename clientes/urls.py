from django.urls import path
from .views import (
    ClienteListView,
    ClienteCreateView,
    ClienteUpdateView,
    ClienteDeleteView,
    cliente_export_csv,
    cliente_export_pdf,
    cliente_print,
)

app_name = 'clientes'

urlpatterns = [
    path('', ClienteListView.as_view(), name='cliente_list'),
    path('nuevo/', ClienteCreateView.as_view(), name='cliente_create'),
    path('editar/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_edit'),
    path('eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_delete'),
    path('exportar/csv/', cliente_export_csv, name='cliente_export_csv'),
    path('exportar/pdf/', cliente_export_pdf, name='cliente_export_pdf'),
    path('imprimir/', cliente_print, name='cliente_print'),
]
