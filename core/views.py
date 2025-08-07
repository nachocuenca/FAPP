from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Cliente, Pedido, Actuacion, Factura
from .forms import ClienteForm, PedidoForm, ActuacionForm, FacturaForm
from .utils import export_csv, export_pdf, render_html



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
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
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
    queryset = Cliente.objects.all()
    fields = [
        ('nombre', 'Nombre'),
        ('email', 'Email'),
        ('telefono', 'Teléfono'),
    ]
    try:
        return export_csv(queryset, fields, 'clientes.csv')
    except Exception as e:
        return HttpResponse(f"Error al generar CSV: {e}", status=500)


@login_required
def cliente_export_pdf(request):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}
    try:
        return export_pdf('core/clientes_pdf.html', context, 'clientes.pdf')
    except Exception as e:
        return HttpResponse(f"Error al generar PDF: {e}", status=500)


@login_required
def cliente_print_html(request):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}
    return render_html('core/clientes_pdf.html', context)

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
    return render(request, 'core/pedidos/pedido_form.html', {'form': form, 'modo': 'nuevo'})

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
    return render(request, 'core/pedidos/pedido_form.html', {'form': form, 'modo': 'editar'})

@login_required
def pedido_export_csv(request):
    queryset = Pedido.objects.all()
    fields = [
        ('fecha', 'Fecha'),
        ('cliente', 'Cliente'),
        ('presupuesto_id', 'Presupuesto'),
        ('total', 'Total'),
    ]
    try:
        return export_csv(queryset, fields, 'pedidos.csv')
    except Exception as e:
        return HttpResponse(f"Error al generar CSV: {e}", status=500)

@login_required
def pedido_export_pdf(request):
    pedidos = Pedido.objects.all()
    context = {'pedidos': pedidos}
    try:
        return export_pdf('core/pedidos/pedidos_pdf.html', context, 'pedidos.pdf')
    except Exception as e:
        return HttpResponse(f"Error al generar PDF: {e}", status=500)


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
            actuacion = form.save(commit=False)
            actuacion.usuario = request.user
            actuacion.save()
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
    queryset = Actuacion.objects.all()
    fields = [
        ('pedido_id', 'Pedido'),
        ('fecha', 'Fecha'),
        ('descripcion', 'Descripción'),
        ('coste', 'Coste'),
    ]
    try:
        return export_csv(queryset, fields, 'actuaciones.csv')
    except Exception as e:
        return HttpResponse(f"Error al generar CSV: {e}", status=500)

# --- Facturas ---
@login_required
def facturas_list(request):
    facturas = Factura.objects.all()
    return render(
        request, "core/facturas/facturas_list.html", {"facturas": facturas}
    )


@login_required
def factura_nueva(request):
    if request.method == "POST":
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.usuario = request.user
            factura.save()
            return redirect("facturas_list")
    else:
        form = FacturaForm()
    return render(request, "core/facturas/factura_form.html", {"form": form})


@login_required
def factura_editar(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    if request.method == "POST":
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            return redirect("facturas_list")
    else:
        form = FacturaForm(instance=factura)
    return render(request, "core/facturas/factura_form.html", {"form": form})


@login_required
def factura_export_csv(request):
    queryset = Factura.objects.all()
    fields = [
        ('numero', 'Número'),
        ('cliente', 'Cliente'),
        ('total', 'Total'),
    ]
    try:
        return export_csv(queryset, fields, 'facturas.csv')
    except Exception as e:
        return HttpResponse(f"Error al generar CSV: {e}", status=500)


@login_required
def factura_export_html(request):
    facturas = Factura.objects.all()
    context = {"facturas": facturas}
    try:
        response = render_html("core/facturas/facturas_export.html", context)
        response["Content-Disposition"] = 'attachment; filename="facturas.html"'
        return response
    except Exception as e:
        return HttpResponse(f"Error al generar HTML: {e}", status=500)


@login_required
def factura_export_pdf(request):
    facturas = Factura.objects.all()
    context = {"facturas": facturas}
    try:
        return export_pdf("core/facturas/facturas_export.html", context, "facturas.pdf")
    except Exception as e:
        return HttpResponse(f"Error al generar PDF: {e}", status=500)
