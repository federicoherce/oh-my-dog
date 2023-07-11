from django import forms
from datetime import date
from .models import PaseadorCuidador, Valoracion
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


class modificarPaseadorCuidador(forms.Form):
    TIPO_CHOICES = [
        ('Paseador', 'Paseador'),
        ('Cuidador', 'Cuidador'),
    ]    
    nomyap = forms.CharField(max_length=30, required=True, label="Nombre y apellido")
    email = forms.EmailField(required=True, error_messages={'unique': 'Ya existe un paseador o cuidador con este email'})
    textolibre = forms.CharField(max_length=200, required=True, label="Texto libre")
    tipo = forms.ChoiceField(choices=TIPO_CHOICES)


class crearValoracion(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ('comentario','puntaje')
        

class ModificarValoracion(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ('comentario','puntaje')
    
class ModificarPaseadorCuidadorSinTipo(forms.Form):
    nomyap = forms.CharField(max_length=30, required=True, label="Nombre y apellido")
    email = forms.EmailField(required=True, error_messages={'unique': 'Ya existe un paseador o cuidador con este email'})
    textolibre = forms.CharField(max_length=200, required=True, label="Texto libre")
    
