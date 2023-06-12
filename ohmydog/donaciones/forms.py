from django import forms
from donaciones.models import Campaña

class CrearCampaña(forms.ModelForm):
    nombre = forms.CharField(max_length=30, required=True)
    monto_objetivo = forms.DecimalField(max_digits=2, required=True)
    descripcion = CharField = forms.CharField(max_length=200, required=True)