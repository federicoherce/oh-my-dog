from django import forms
from datetime import date
from .models import PaseadorCuidador
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class CrearPaseadorCuidador(forms.ModelForm):
    class Meta:
        model = PaseadorCuidador
        fields = ('nomyap', 'dni', 'textolibre', 'tipo',)

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
    nomyap = forms.CharField(max_length=30, required=True)
    dni = forms.CharField(max_length=8, required=True, validators=[
            RegexValidator(r'^[0-9]{8}$', 'El DNI debe tener 8 dígitos.')], error_messages= {
            'unique': 'Ya existe un usuario con este DNI'})
    textolibre = forms.CharField(max_length=200, required=True)
    tipo = forms.ChoiceField(choices=TIPO_CHOICES)