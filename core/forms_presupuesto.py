
from django import forms
from .models import Presupuesto

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['numero', 'cliente', 'concepto', 'total', 'estado']
        widgets = {
            'concepto': forms.Textarea(attrs={'rows': 3}),
        }
