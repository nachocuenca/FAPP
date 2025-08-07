import csv
from django.http import HttpResponse
from .models import Cliente
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def cliente_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'CIF', 'Email', 'Teléfono', 'Activo'])


    clientes = Cliente.objects.filter(usuario=request.user)
    for c in clientes:

        writer.writerow([c.nombre, c.cif, c.email, c.telefono, 'Sí' if c.activo else 'No'])


    return response

@login_required
def cliente_export_pdf(request):
    clientes = Cliente.objects.filter(usuario=request.user)
    template = get_template('core/clientes_pdf.html')
    html = template.render({'clientes': clientes})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="clientes.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response
