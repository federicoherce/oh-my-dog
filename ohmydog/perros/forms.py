from django import forms
from datetime import date
from .models import Perro

RAZAS_PERRO = [
        ('labrador', 'Labrador'),
        ('bulldog', 'Bulldog'),
        ('pitbull', 'Pitbull'),
        ('boxer', 'Boxer'),
        ('pastor', 'Pastor aleman'),
        ('beagle', 'Beagle'),
        ('golden', 'Golden retriever'),
        ('fox', 'Fox Terrier'),
        ('esquimal', 'Esquimal canadiense'),
        ('dalmata', 'Dalmata'),
        ('yorkshire', 'Yorkshire terrier'),
        ('siberiano', 'Siberiano'),
        ('caniche', 'Caniche'),
        ('chihuahua', 'Chihuaha')
    ]

SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra')
    ]


class CrearPerro(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=50)
    raza = forms.ChoiceField(label="Raza", choices=RAZAS_PERRO)
    color = forms.CharField(label="Color", max_length=50)
    fecha_de_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'max': str(date.today())}),
        input_formats=['%Y-%m-%d']
    )
    sexo = forms.ChoiceField(label="Sexo", choices=SEXO_CHOICES, widget=forms.RadioSelect)

    class Meta():
        model = Perro
        fields = ('nombre', 'raza', 'color', 'fecha_de_nacimiento', 'sexo')
    