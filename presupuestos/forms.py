from django import forms
from core.models import Presupuesto

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['cliente', 'fecha', 'concepto', 'total']
        widgets = {
            'concepto': forms.Textarea(attrs={'rows': 3}),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
