from django import forms
from .models import Perdidos
from django.db import models


class PublicarPerroPerdido(forms.ModelForm):
    class Meta:
        model = Perdidos
        exclude = ['telefono', 'encontrado']

class ModificarPerroPerdido(forms.ModelForm):
    class Meta:
        model = Perdidos
        exclude = ['telefono', 'encontrado', 'imagen']
        
class ModificarImagen(forms.Form):
    imagen = forms.ImageField()
    