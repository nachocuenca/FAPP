
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Presupuesto
from .forms import PresupuestoForm

@login_required
def presupuestos_list(request):
    presupuestos = Presupuesto.objects.all()
    return render(request, 'core/presupuestos/presupuestos_list.html', {'presupuestos': presupuestos})

@login_required
def presupuesto_nuevo(request):
    form = PresupuestoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('presupuestos_list')
    return render(request, 'core/presupuestos/presupuesto_form.html', {'form': form, 'modo': 'Nuevo'})

@login_required
def presupuesto_editar(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    form = PresupuestoForm(request.POST or None, instance=presupuesto)
    if form.is_valid():
        form.save()
        return redirect('presupuestos_list')
    return render(request, 'core/presupuestos/presupuesto_form.html', {'form': form, 'modo': 'Editar'})

@login_required
def presupuesto_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="presupuestos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Número', 'Cliente', 'Total', 'Estado'])
    for p in Presupuesto.objects.all():
        writer.writerow([p.fecha, p.numero, p.cliente.nombre, p.total, p.estado])
    return response

@login_required
def presupuesto_export_pdf(request):
    presupuestos = Presupuesto.objects.all()
    template = get_template('core/presupuestos/presupuestos_pdf.html')
    html = template.render({'presupuestos': presupuestos})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="presupuestos.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response
