
from django.urls import path
from . import views

urlpatterns = [
    path('presupuestos/', views.presupuestos_list, name='presupuestos_list'),
    path('presupuestos/nuevo/', views.presupuesto_nuevo, name='presupuesto_nuevo'),
    path('presupuestos/editar/<int:pk>/', views.presupuesto_editar, name='presupuesto_editar'),
    path('presupuestos/export/csv/', views.presupuesto_export_csv, name='presupuesto_export_csv'),
    path('presupuestos/export/pdf/', views.presupuesto_export_pdf, name='presupuesto_export_pdf'),
]
