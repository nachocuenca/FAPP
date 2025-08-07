from django.urls import path
from core import views

urlpatterns = [
    path('', views.facturas_list, name='facturas_list'),
    path('nueva/', views.factura_nueva, name='factura_nueva'),
    path('editar/<int:pk>/', views.factura_editar, name='factura_editar'),
    path('export/csv/', views.factura_export_csv, name='factura_export_csv'),
    path('export/html/', views.factura_export_html, name='factura_export_html'),
    path('export/pdf/', views.factura_export_pdf, name='factura_export_pdf'),
]
