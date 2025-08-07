from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Cliente, Presupuesto, Pedido, Actuacion, Factura
from .forms import ClienteForm, PresupuestoForm, PedidoForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
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
    queryset = Cliente.objects.all()
    fields = [
        ('nombre', 'Nombre'),
        ('email', 'Email'),
        ('telefono', 'Teléfono'),
    ]
    return export_csv(queryset, fields, 'clientes.csv')


@login_required
def cliente_export_pdf(request):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}
    return export_pdf('core/clientes_pdf.html', context, 'clientes.pdf')


@login_required
def cliente_print_html(request):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}
    return render_html('core/clientes_pdf.html', context)

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
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pedidos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Cliente', 'Presupuesto', 'Total'])
    for p in Pedido.objects.all():
        writer.writerow([p.fecha, p.cliente.nombre, p.presupuesto.id if p.presupuesto else '', p.total])
    return response

@login_required
def pedido_export_pdf(request):
    pedidos = Pedido.objects.all()
    template = get_template('core/pedidos/pedidos_pdf.html')
    html = template.render({'pedidos': pedidos})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pedidos.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

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
