from django.urls import path
from core import views

urlpatterns = [
    path('', views.pedidos_list, name='pedidos_list'),
    path('nuevo/', views.pedido_nuevo, name='pedido_nuevo'),
    path('editar/<int:pk>/', views.pedido_editar, name='pedido_editar'),
    path('export/csv/', views.pedido_export_csv, name='pedido_export_csv'),
    path('export/pdf/', views.pedido_export_pdf, name='pedido_export_pdf'),
]
