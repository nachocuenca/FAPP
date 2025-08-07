import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Presupuesto

@login_required
def presupuesto_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="presupuestos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Número', 'Cliente', 'Total', 'Estado'])

    presupuestos = Presupuesto.objects.all()
    for p in presupuestos:
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
