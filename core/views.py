from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from pedidos.models import Pedido
from actuaciones.models import Actuacion
from facturas.models import Factura
from django.template.loader import render_to_string
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pedidos.forms import PedidoForm
from actuaciones.forms import ActuacionForm
from facturas.forms import FacturaForm
from .utils import export_csv, export_pdf


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

# --- Pedidos ---
@login_required
def pedidos_list(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'pedidos/pedidos_list.html', {'pedidos': pedidos})

@login_required
def pedido_nuevo(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST, request=request)
        if form.is_valid():
            pedido = form.save(commit=False)
            cliente = form.cleaned_data["cliente"]
            if cliente.usuario != request.user:
                return HttpResponseForbidden()
            presupuesto = form.cleaned_data.get("presupuesto")
            if presupuesto and presupuesto.usuario != request.user:
                return HttpResponseForbidden()
            pedido.usuario = request.user
            pedido.save()
            return redirect('pedidos_list')
    else:
        form = PedidoForm(request=request)
    return render(request, 'pedidos/pedido_form.html', {'form': form, 'modo': 'nuevo'})

@login_required
def pedido_editar(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido, request=request)
        if form.is_valid():
            form.save()
            return redirect('pedidos_list')
    else:
        form = PedidoForm(instance=pedido, request=request)
    return render(request, 'pedidos/pedido_form.html', {'form': form, 'modo': 'editar'})

@login_required
def pedido_export_csv(request):
    queryset = Pedido.objects.filter(usuario=request.user)
    fields = [
        ("fecha", "Fecha"),
        ("cliente", "Cliente"),
        ("presupuesto", "Presupuesto"),
        ("total", "Total"),
    ]
    try:
        return export_csv(queryset, fields, "pedidos.csv")
    except Exception as e:
        return HttpResponse(f"Error al generar CSV: {e}", status=500)

@login_required
def pedido_export_pdf(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    context = {"pedidos": pedidos}
    try:
        return export_pdf("pedidos/pedidos_pdf.html", context, "pedidos.pdf")
    except Exception as e:
        return HttpResponse(f"Error al generar PDF: {e}", status=500)


# --- Actuaciones ---
@login_required
def actuaciones_list(request):
    actuaciones = Actuacion.objects.filter(usuario=request.user)
    return render(request, 'actuaciones/actuaciones_list.html', {'actuaciones': actuaciones})

@login_required
def actuacion_nueva(request):
    if request.method == 'POST':
        form = ActuacionForm(request.POST, request=request)
        if form.is_valid():
            actuacion = form.save(commit=False)
            cliente = form.cleaned_data["cliente"]
            pedido = form.cleaned_data["pedido"]
            if cliente.usuario != request.user or pedido.usuario != request.user:
                return HttpResponseForbidden()
            actuacion.usuario = request.user
            actuacion.save()
            return redirect('actuaciones_list')
    else:
        form = ActuacionForm(request=request)
    return render(request, 'actuaciones/actuacion_form.html', {'form': form})

@login_required
def actuacion_editar(request, pk):
    actuacion = get_object_or_404(Actuacion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ActuacionForm(request.POST, instance=actuacion, request=request)
        if form.is_valid():
            form.save()
            return redirect('actuaciones_list')
    else:
        form = ActuacionForm(instance=actuacion, request=request)
    return render(request, 'actuaciones/actuacion_form.html', {'form': form})

@login_required
def actuacion_eliminar(request, pk):
    actuacion = get_object_or_404(Actuacion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        actuacion.delete()
        return redirect('actuaciones_list')
    return render(request, 'actuaciones/actuacion_confirm_delete.html', {'actuacion': actuacion})

@login_required
def actuaciones_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="actuaciones.csv"'
    writer = csv.writer(response)
    writer.writerow(['Pedido', 'Fecha', 'Descripción', 'Coste'])
    for act in Actuacion.objects.filter(usuario=request.user):
        writer.writerow([act.pedido.id, act.fecha, act.descripcion, act.coste])
    return response

# --- Facturas ---
@login_required
def facturas_list(request):
    facturas = Factura.objects.filter(usuario=request.user)
    return render(
        request, "facturas/facturas_list.html", {"facturas": facturas}
    )


@login_required
def factura_nueva(request):
    if request.method == "POST":
        form = FacturaForm(request.POST, request=request)
        if form.is_valid():
            factura = form.save(commit=False)
            cliente = form.cleaned_data["cliente"]
            pedido = form.cleaned_data.get("pedido")
            actuacion = form.cleaned_data.get("actuacion")
            if cliente.usuario != request.user:
                return HttpResponseForbidden()
            if pedido and pedido.usuario != request.user:
                return HttpResponseForbidden()
            if actuacion and actuacion.usuario != request.user:
                return HttpResponseForbidden()
            factura.usuario = request.user
            factura.save()
            return redirect("facturas_list")
    else:
        form = FacturaForm(request=request)
    return render(request, "facturas/factura_form.html", {"form": form})


@login_required
def factura_editar(request, pk):
    factura = get_object_or_404(Factura, pk=pk, usuario=request.user)
    if request.method == "POST":
        form = FacturaForm(request.POST, instance=factura, request=request)
        if form.is_valid():
            form.save()
            return redirect("facturas_list")
    else:
        form = FacturaForm(instance=factura, request=request)
    return render(request, "facturas/factura_form.html", {"form": form})


@login_required
def factura_export_csv(request):
    queryset = Factura.objects.filter(usuario=request.user)
    fields = [
        ("numero", "Número"),
        ("cliente", "Cliente"),
        ("total", "Total"),
    ]
    try:
        return export_csv(queryset, fields, "facturas.csv")
    except Exception as e:
        return HttpResponse(f"Error al generar CSV: {e}", status=500)



@login_required
def factura_export_html(request):
    facturas = Factura.objects.filter(usuario=request.user)
    html = render_to_string(
        "facturas/facturas_export.html", {"facturas": facturas}
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
    for factura in Factura.objects.filter(usuario=request.user):
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

