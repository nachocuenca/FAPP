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
        fields = ['cliente', 'fecha', 'descripcion', 'total']
        labels = {
            'cliente': 'Cliente',
            'fecha': 'Fecha',
            'descripcion': 'Descripción',
            'total': 'Total (€)',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ActuacionForm(forms.ModelForm):
    class Meta:
        model = Actuacion
        fields = ['cliente', 'fecha', 'descripcion', 'pedido', 'total']
        labels = {
            'cliente': 'Cliente',
            'fecha': 'Fecha',
            'descripcion': 'Descripción del servicio',
            'pedido': 'Pedido asociado',
            'total': 'Total (€)',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pedido': forms.Select(attrs={'class': 'form-select'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class FacturaForm(forms.ModelForm):
    total = forms.DecimalField(label='Total (€)', required=False, disabled=True)
    class Meta:
        model = Factura
        fields = [
            'cliente',
            'pedido',
            'actuacion',
            'fecha',
            'numero',
            'base_imponible',
            'iva',
            'irpf',
        ]
        labels = {
            'cliente': 'Cliente',
            'pedido': 'Pedido',
            'actuacion': 'Actuación',
            'fecha': 'Fecha',
            'numero': 'Número',
            'base_imponible': 'Base imponible (€)',
            'iva': 'IVA (%)',
            'irpf': 'IRPF (%)',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'pedido': forms.Select(attrs={'class': 'form-select'}),
            'actuacion': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'base_imponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'iva': forms.NumberInput(attrs={'class': 'form-control'}),
            'irpf': forms.NumberInput(attrs={'class': 'form-control'}),
        }
