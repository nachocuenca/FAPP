
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente, Presupuesto, Pedido, Actuacion, Factura
from .forms import ClienteForm, PresupuestoForm, PedidoForm, ActuacionForm
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

# --- Presupuestos ---
@login_required
def presupuestos_list(request):
    presupuestos = Presupuesto.objects.all()
    return render(request, 'core/presupuestos/presupuestos_list.html', {'presupuestos': presupuestos})

@login_required
def presupuesto_nuevo(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('presupuestos_list')
    else:
        form = PresupuestoForm()
    return render(request, 'core/presupuestos/presupuesto_form.html', {'form': form})

@login_required
def presupuesto_editar(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    if request.method == 'POST':
        form = PresupuestoForm(request.POST, instance=presupuesto)
        if form.is_valid():
            form.save()
            return redirect('presupuestos_list')
    else:
        form = PresupuestoForm(instance=presupuesto)
    return render(request, 'core/presupuestos/presupuesto_form.html', {'form': form})

@login_required
def presupuesto_export_csv(request):
    return HttpResponse("Exportar CSV (presupuestos)")

@login_required
def presupuesto_export_pdf(request):
    return HttpResponse("Exportar PDF (presupuestos)")

# --- Pedidos ---
@login_required
def pedidos_list(request):
    pedidos = Pedido.objects.all()
    return render(request, 'core/pedidos/pedidos_list.html', {'pedidos': pedidos})

@login_required
def pedido_nuevo(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.save()
            return redirect('pedidos_list')
    else:
        form = PedidoForm()
    return render(request, 'core/pedidos/pedido_form.html', {'form': form})

@login_required
def pedido_editar(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('pedidos_list')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'core/pedidos/pedido_form.html', {'form': form})

# --- Actuaciones ---
@login_required
def actuaciones_list(request):
    actuaciones = Actuacion.objects.all()
    return render(request, 'core/actuaciones/actuaciones_list.html', {'actuaciones': actuaciones})

@login_required
def actuacion_nueva(request):
    if request.method == 'POST':
        form = ActuacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('actuaciones_list')
    else:
        form = ActuacionForm()
    return render(request, 'core/actuaciones/actuacion_form.html', {'form': form})

@login_required
def actuacion_editar(request, pk):
    actuacion = get_object_or_404(Actuacion, pk=pk)
    if request.method == 'POST':
        form = ActuacionForm(request.POST, instance=actuacion)
        if form.is_valid():
            form.save()
            return redirect('actuaciones_list')
    else:
        form = ActuacionForm(instance=actuacion)
    return render(request, 'core/actuaciones/actuacion_form.html', {'form': form})

@login_required
def actuacion_eliminar(request, pk):
    actuacion = get_object_or_404(Actuacion, pk=pk)
    if request.method == 'POST':
        actuacion.delete()
        return redirect('actuaciones_list')
    return render(request, 'core/actuaciones/actuacion_confirm_delete.html', {'actuacion': actuacion})

@login_required
def actuaciones_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="actuaciones.csv"'
    writer = csv.writer(response)
    writer.writerow(['Pedido', 'Fecha', 'Descripción', 'Coste'])
    for act in Actuacion.objects.all():
        writer.writerow([act.pedido.id, act.fecha, act.descripcion, act.coste])
    return response

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
