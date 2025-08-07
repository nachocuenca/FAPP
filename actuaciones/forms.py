from django import forms
from clientes.models import Cliente
from pedidos.models import Pedido
from .models import Actuacion


class ActuacionForm(forms.ModelForm):
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

    class Meta:
        model = Actuacion
        fields = ['cliente', 'pedido', 'fecha', 'descripcion', 'coste']
        labels = {
            'cliente': 'Cliente',
            'pedido': 'Pedido asociado',
            'fecha': 'Fecha',
            'descripcion': 'Descripción del servicio',
            'coste': 'Coste',
        }
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'pedido': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'coste': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_coste(self):
        coste = self.cleaned_data.get('coste')
        if coste is not None and coste < 0:
            raise forms.ValidationError('El coste debe ser mayor o igual a cero.')
        return coste
