from django import forms
from datetime import date
from .models import PaseadorCuidador
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class CrearPaseadorCuidador(forms.ModelForm):
    class Meta:
        model = PaseadorCuidador
        fields = ('nomyap', 'email', 'textolibre', 'tipo',)
        labels = {
            'nomyap': _('Nombre y apellido'),
            'textolibre' : ('Texto libre'),
        }

#class CrearPaseadorCuidador(forms.Form):
#    TIPO_CHOICES = [
#        ('P', 'Paseador'),
#        ('C', 'Cuidador'),
#    ] 
#    nomyap = forms.CharField(label="Nombre y Apellido", max_length=50)
#    dni = forms.CharField(max_length=8, required=True, validators=[
#            RegexValidator(r'^[0-9]{8}$', 'El DNI debe tener 8 dígitos.')], error_messages= {
#           'unique': 'Ya existe un usuario con este DNI'})
#    textolibre = forms.CharField(label="Descripcion", max_length=50)
#    tipo = forms.ChoiceField(choices=TIPO_CHOICES)
#
#    class Meta():
#        model = PaseadorCuidador
#        fields = ('nomyap', 'dni', 'textolibre', 'tipo')



class modificarPaseadorCuidador(forms.Form):
    TIPO_CHOICES = [
        ('Paseador', 'Paseador'),
        ('Cuidador', 'Cuidador'),
    ]    
    nomyap = forms.CharField(max_length=30, required=True, label="Nombre y apellido")
    email = forms.EmailField(required=True, error_messages={'unique': 'Ya existe un paseador o cuidador con este email'})
    textolibre = forms.CharField(max_length=200, required=True, label="Texto libre")
    tipo = forms.ChoiceField(choices=TIPO_CHOICES)
    
class ModificarPaseadorCuidadorSinTipo(forms.Form):
    nomyap = forms.CharField(max_length=30, required=True, label="Nombre y apellido")
    email = forms.EmailField(required=True, error_messages={'unique': 'Ya existe un paseador o cuidador con este email'})
    textolibre = forms.CharField(max_length=200, required=True, label="Texto libre")
    