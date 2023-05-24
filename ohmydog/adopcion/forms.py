from django import forms
from .models import Adopcion


class PublicarPerroEnAdopcion(forms.ModelForm):
    class Meta:
        model = Adopcion
        exclude = ['publicado_por', 'adoptado']

class AdopcionForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
            attrs={'placeholder': 'Correo Electrónico'}))
        