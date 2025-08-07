from django.urls import path
from core import views

urlpatterns = [
    path('', views.actuaciones_list, name='actuaciones_list'),
    path('nueva/', views.actuacion_nueva, name='actuacion_nueva'),
    path('editar/<int:pk>/', views.actuacion_editar, name='actuacion_editar'),
    path('eliminar/<int:pk>/', views.actuacion_eliminar, name='actuacion_eliminar'),
    path('export/csv/', views.actuaciones_export_csv, name='actuaciones_export_csv'),
]
