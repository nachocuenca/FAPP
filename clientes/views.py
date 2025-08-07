from io import BytesIO
import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required

from .forms import ClienteForm
from core.models import Cliente

@login_required
def cliente_list(request):
    clientes = Cliente.objects.filter(usuario=request.user)
    return render(request, 'clientes/cliente_list.html', {'clientes': clientes})


@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            return redirect('clientes:cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form})


@login_required
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            return redirect('clientes:cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form})


@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, usuario=request.user)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes:cliente_list')
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})


@login_required
def cliente_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Email', 'Telefono', 'Direccion'])
    for c in Cliente.objects.filter(usuario=request.user):
        writer.writerow([c.nombre, c.email, c.telefono, c.direccion])
    return response


@login_required
def cliente_export_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    y = 800
    for c in Cliente.objects.filter(usuario=request.user):
        p.drawString(50, y, f"{c.nombre} - {c.email or ''} - {c.telefono or ''}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 800
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


@login_required
def cliente_print(request):
    clientes = Cliente.objects.filter(usuario=request.user)
    return render(request, 'clientes/clientes_print.html', {'clientes': clientes})
