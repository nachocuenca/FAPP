from django.urls import path
from . import views

urlpatterns = [
    path('', views.presupuesto_list, name='presupuesto_list'),
    path('nuevo/', views.presupuesto_create, name='presupuesto_create'),
    path('<int:pk>/editar/', views.presupuesto_update, name='presupuesto_update'),
    path('<int:pk>/eliminar/', views.presupuesto_delete, name='presupuesto_delete'),
    path('export/csv/', views.presupuesto_export_csv, name='presupuesto_export_csv'),
    path('export/pdf/', views.presupuesto_export_pdf, name='presupuesto_export_pdf'),
    path('export/html/', views.presupuesto_export_html, name='presupuesto_export_html'),
]
