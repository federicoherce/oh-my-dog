from django import forms
from datetime import date
from .models import PaseadorCuidador

class CrearPaseadorCuidador(forms.Form):
    nomyap = forms.CharField(label="Nombre y Apellido", max_length=50)
    dni = forms.CharField(label="DNI", max_length=50)
    textolibre = forms.CharField(label="Descripcion", max_length=50)

    class Meta():
        model = PaseadorCuidador
        fields = ('nomyap', 'dni', 'textolibre')
    