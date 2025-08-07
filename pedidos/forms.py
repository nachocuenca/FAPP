from django import forms
from clientes.models import Cliente
from presupuestos.models import Presupuesto
from .models import Pedido


class PedidoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields['cliente'].queryset = Cliente.objects.filter(
                usuario=self.request.user
            )
            self.fields['presupuesto'].queryset = Presupuesto.objects.filter(
                usuario=self.request.user
            )

    class Meta:
        model = Pedido
        fields = ['cliente', 'presupuesto', 'fecha', 'descripcion', 'total']
        labels = {
            'cliente': 'Cliente',
            'presupuesto': 'Presupuesto',
            'fecha': 'Fecha',
            'descripcion': 'Descripción',
            'total': 'Total',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'presupuesto': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is not None and total < 0:
            raise forms.ValidationError('El total debe ser mayor o igual a cero.')
        return total
