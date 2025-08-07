from io import BytesIO
import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from reportlab.pdfgen import canvas
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import ClienteForm
from .models import Cliente


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:cliente_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:cliente_list')

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:cliente_list')

    def get_queryset(self):
        return Cliente.objects.filter(usuario=self.request.user)


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
