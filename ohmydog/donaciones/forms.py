from django import forms
from donaciones.models import Campaña, Donacion

class CrearCampaña(forms.ModelForm):
    class Meta:
        model = Campaña
        fields = ['nombre', 'monto_objetivo', 'descripcion']

class CrearDonacion(forms.ModelForm):
    nombre = forms.CharField(label='Nombre (opcional)', required=False)
    
    class Meta:
        model = Donacion
        fields = ['monto', 'nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre'}),
        }