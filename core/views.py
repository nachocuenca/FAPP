from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente, Pedido, Actuacion, Factura
from .forms import ClienteForm, PedidoForm, ActuacionForm, FacturaForm
from django.http import HttpResponse
import csv

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

# --- Clientes ---
@login_required
def clientes_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'core/clientes/clientes_list.html', {'clientes': clientes})

@login_required
def cliente_nuevo(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm()
    return render(request, 'core/clientes/cliente_form.html', {'form': form})

@login_required
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'core/clientes/cliente_form.html', {'form': form})

@login_required
def cliente_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Email', 'Teléfono'])
    for cliente in Cliente.objects.all():
        writer.writerow([cliente.nombre, cliente.email, cliente.telefono])
    return response

# --- Pedidos ---
@login_required
def pedidos_list(request):
    return render(request, 'core/pedidos/pedidos_list.html')

@login_required
def pedido_nuevo(request):
    return render(request, 'core/pedidos/pedido_form.html')

@login_required
def pedido_editar(request, pk):
    return render(request, 'core/pedidos/pedido_form.html')

# --- Actuaciones ---
@login_required
def actuaciones_list(request):
    return render(request, 'core/actuaciones/actuaciones_list.html')

@login_required
def actuacion_nueva(request):
    return render(request, 'core/actuaciones/actuacion_form.html')

@login_required
def actuacion_editar(request, pk):
    return render(request, 'core/actuaciones/actuacion_form.html')

# --- Facturas ---
@login_required
def facturas_list(request):
    return render(request, 'core/facturas/facturas_list.html')

@login_required
def factura_nueva(request):
    return render(request, 'core/facturas/factura_form.html')

@login_required
def factura_editar(request, pk):
    return render(request, 'core/facturas/factura_form.html')

@login_required
def factura_export_csv(request):
    return HttpResponse("Exportar CSV (facturas)")

@login_required
def factura_export_pdf(request):
    return HttpResponse("Exportar PDF (facturas)")
