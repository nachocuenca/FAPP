from django.urls import include, path
from django.http import HttpResponse


def dummy_view(request):
    return HttpResponse("")

urlpatterns = [
    path('', include(('clientes.urls', 'clientes'), namespace='clientes')),
    path('logout/', dummy_view, name='logout'),
    path('dashboard/', dummy_view, name='dashboard'),
    path('clientes-list/', dummy_view, name='clientes_list'),
    path('presupuestos/', dummy_view, name='presupuestos_list'),
]
