
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente, Presupuesto, Pedido, Actuacion, Factura
from .forms import ClienteForm, PresupuestoForm, FacturaForm
from django.http import HttpResponse
from django.template.loader import render_to_string
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

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
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="facturas.csv"'
    writer = csv.writer(response)
    writer.writerow(["Número", "Cliente", "Total"])
    for factura in Factura.objects.all():
        writer.writerow([factura.numero, factura.cliente.nombre, factura.total])
    return response


@login_required
def factura_export_html(request):
    facturas = Factura.objects.all()
    html = render_to_string(
        "core/facturas/facturas_export.html", {"facturas": facturas}
    )
    response = HttpResponse(html, content_type="text/html")
    response["Content-Disposition"] = 'attachment; filename="facturas.html"'
    return response


@login_required
def factura_export_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="facturas.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    y = 770
    p.drawString(80, 800, "Listado de facturas")
    for factura in Factura.objects.all():
        p.drawString(
            80,
            y,
            f"{factura.numero} - {factura.cliente.nombre} - {factura.total}",
        )
        y -= 20
        if y < 50:
            p.showPage()
            y = 770
    p.showPage()
    p.save()
    return response
