from django import forms
from .models import Cliente, Presupuesto, Pedido, Actuacion, Factura


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'direccion', 'activo']
        labels = {
            'nombre': 'Nombre completo',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'activo': '¿Activo?',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['cliente', 'fecha', 'concepto', 'total']
        labels = {
            'cliente': 'Cliente',
            'fecha': 'Fecha',
            'concepto': 'Concepto',
            'total': 'Importe total (€)',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'concepto': forms.TextInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'fecha', 'descripcion', 'estado']
        labels = {
            'cliente': 'Cliente',
            'fecha': 'Fecha',
            'descripcion': 'Descripción',
            'estado': 'Estado',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }


class ActuacionForm(forms.ModelForm):
    class Meta:
        model = Actuacion
        fields = ['cliente', 'fecha', 'descripcion', 'tecnico', 'estado']
        labels = {
            'cliente': 'Cliente',
            'fecha': 'Fecha',
            'descripcion': 'Descripción del servicio',
            'tecnico': 'Técnico asignado',
            'estado': 'Estado',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tecnico': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente', 'fecha', 'concepto', 'base_imponible', 'iva', 'total']
        labels = {
            'cliente': 'Cliente',
            'fecha': 'Fecha',
            'concepto': 'Concepto',
            'base_imponible': 'Base imponible (€)',
            'iva': 'IVA (%)',
            'total': 'Total (€)',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'concepto': forms.TextInput(attrs={'class': 'form-control'}),
            'base_imponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'iva': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
