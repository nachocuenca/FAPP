from django import forms
from clientes.models import Cliente
from pedidos.models import Pedido
from actuaciones.models import Actuacion
from .models import Factura


class FacturaForm(forms.ModelForm):
    total = forms.DecimalField(
        label='Total (€)', required=False, disabled=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields['cliente'].queryset = Cliente.objects.filter(
                usuario=self.request.user
            )
            self.fields['pedido'].queryset = Pedido.objects.filter(
                usuario=self.request.user
            )
            self.fields['actuacion'].queryset = Actuacion.objects.filter(
                usuario=self.request.user
            )

    class Meta:
        model = Factura
        fields = ['cliente', 'pedido', 'actuacion', 'fecha', 'numero', 'base_imponible', 'iva', 'irpf', 'estado']
        labels = {
            'cliente': 'Cliente',
            'pedido': 'Pedido',
            'actuacion': 'Actuación',
            'fecha': 'Fecha',
            'numero': 'Número',
            'base_imponible': 'Base imponible (€)',
            'iva': 'IVA (%)',
            'irpf': 'IRPF (%)',
            'estado': 'Estado',
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
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_base_imponible(self):
        base_imponible = self.cleaned_data.get('base_imponible')
        if base_imponible is not None and base_imponible < 0:
            raise forms.ValidationError('La base imponible debe ser mayor o igual a cero.')
        return base_imponible

    def clean_iva(self):
        iva = self.cleaned_data.get('iva')
        if iva is not None and iva < 0:
            raise forms.ValidationError('El IVA debe ser mayor o igual a cero.')
        return iva

    def clean_irpf(self):
        irpf = self.cleaned_data.get('irpf')
        if irpf is not None and irpf < 0:
            raise forms.ValidationError('El IRPF debe ser mayor o igual a cero.')
        return irpf
