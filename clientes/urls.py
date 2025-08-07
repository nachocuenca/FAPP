from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.cliente_list, name='cliente_list'),
    path('nuevo/', views.cliente_create, name='cliente_create'),
    path('editar/<int:pk>/', views.cliente_edit, name='cliente_edit'),
    path('eliminar/<int:pk>/', views.cliente_delete, name='cliente_delete'),
    path('exportar/csv/', views.cliente_export_csv, name='cliente_export_csv'),
    path('exportar/pdf/', views.cliente_export_pdf, name='cliente_export_pdf'),
    path('imprimir/', views.cliente_print, name='cliente_print'),
]
