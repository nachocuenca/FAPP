from django import forms
from core.models import Presupuesto, Cliente

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
