from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Clientes
    path('clientes/', views.clientes_list, name='clientes_list'),
    path('clientes/nuevo/', views.cliente_nuevo, name='cliente_nuevo'),
    path('clientes/editar/<int:pk>/', views.cliente_editar, name='cliente_editar'),
    path('clientes/export/csv/', views.cliente_export_csv, name='cliente_export_csv'),
    path('clientes/export/pdf/', views.cliente_export_pdf, name='cliente_export_pdf'),
    path('clientes/print/html/', views.cliente_print_html, name='cliente_print_html'),

    # Pedidos
    path('pedidos/', views.pedidos_list, name='pedidos_list'),
    path('pedidos/nuevo/', views.pedido_nuevo, name='pedido_nuevo'),
    path('pedidos/editar/<int:pk>/', views.pedido_editar, name='pedido_editar'),
    path('pedidos/export/csv/', views.pedido_export_csv, name='pedido_export_csv'),
    path('pedidos/export/pdf/', views.pedido_export_pdf, name='pedido_export_pdf'),

    # Actuaciones
    path('actuaciones/', views.actuaciones_list, name='actuaciones_list'),
    path('actuaciones/nueva/', views.actuacion_nueva, name='actuacion_nueva'),
    path('actuaciones/editar/<int:pk>/', views.actuacion_editar, name='actuacion_editar'),

    # Facturas
    path('facturas/', views.facturas_list, name='facturas_list'),
    path('facturas/nueva/', views.factura_nueva, name='factura_nueva'),
    path('facturas/editar/<int:pk>/', views.factura_editar, name='factura_editar'),
    path('facturas/export/csv/', views.factura_export_csv, name='factura_export_csv'),
    path('facturas/export/pdf/', views.factura_export_pdf, name='factura_export_pdf'),
]
