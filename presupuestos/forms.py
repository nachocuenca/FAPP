from django import forms
from clientes.models import Cliente
from .models import Presupuesto

class PresupuestoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields['cliente'].queryset = Cliente.objects.filter(
                usuario=self.request.user
            )

    class Meta:
        model = Presupuesto
        fields = ['cliente', 'fecha', 'concepto', 'total']
        widgets = {
            'concepto': forms.Textarea(attrs={'rows': 3}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is not None and total < 0:
            raise forms.ValidationError('El total debe ser mayor o igual a cero.')
        return total
