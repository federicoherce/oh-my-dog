from django import forms
from donaciones.models import Campaña, Donacion

class CrearCampaña(forms.ModelForm):
    class Meta:
        model = Campaña
        fields = ['nombre', 'monto_objetivo', 'descripcion']

class CrearDonacion(forms.ModelForm):
    class Meta:
        model = Donacion
        fields = ['monto', 'nombre']