from django import forms
from donaciones.models import Campaña, Donacion

class CrearCampaña(forms.ModelForm):
    class Meta:
        model = Campaña
        fields = ['nombre', 'monto_objetivo', 'descripcion']

class CrearDonacionCampaña(forms.ModelForm):
    nombre = forms.CharField(label='Nombre (opcional)', required=False)

    class Meta:
        model = Donacion
        fields = ['monto', 'nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre'}),
        }

class CrearDonacionVeterinaria(forms.ModelForm):
    nombre = forms.CharField(label='Nombre (opcional)', required=False)
    motivo = forms.CharField(max_length=200, label='Motivo (opcional)', required=False)

    class Meta:
        model = Donacion
        fields = ['monto', 'nombre', 'motivo']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre'}),
        }