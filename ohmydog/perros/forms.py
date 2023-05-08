from django import forms
from datetime import date
from .models import Perro

class CrearPerro(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=50)
    raza = forms.CharField(label="Raza", max_length=50)
    color = forms.CharField(label="Color", max_length=50)
    fecha_de_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'max': str(date.today())}),
        input_formats=['%Y-%m-%d']
    )

    class Meta():
        model = Perro
        fields = ('nombre', 'raza', 'color', 'fecha_de_nacimiento',)
    