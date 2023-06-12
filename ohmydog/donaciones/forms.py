from django import forms
from donaciones.models import Campaña

class CrearCampaña(forms.ModelForm):
    class Meta:
        model = Campaña
        exclude = ['nombre', 'monto_objetivo', 'descripcion']
    #nombre = forms.CharField(max_length=30, required=True, unique=True, error_messages={
    #        'unique': 'Ya existe un usuario con este email'})
    #monto_objetivo = forms.DecimalField(max_digits=2, required=True)
    #descripcion = CharField = forms.CharField(max_length=200, required=True)