from django import forms
from .models import Perdidos
from django.db import models


class PublicarPerroPerdido(forms.ModelForm):
    class Meta:
        model = Perdidos
        exclude = ['telefono', 'encontrado']
    observacion = forms.CharField(max_length=200, label='Observacion (opcional)', required=False)

class ModificarPerroPerdido(forms.ModelForm):
    class Meta:
        model = Perdidos
        exclude = ['telefono', 'encontrado', 'imagen']
    observacion = forms.CharField(max_length=200, label='Observacion (opcional)', required=False)

        
class ModificarImagen(forms.Form):
    imagen = forms.ImageField()
    