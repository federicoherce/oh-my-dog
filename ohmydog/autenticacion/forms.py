from django import forms
from django.db import models 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):    
    class Meta:
        model = CustomUser
        fields = ('email', 'nombre', 'apellido', 'dni', 'telefono',)
        
        
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("email"),
        widget=forms.TextInput(attrs={'autofocus': True}),
    )

class FiltrosDeListadoDeClientes(forms.Form):
    nombre = forms.CharField(required=False)
    apellido = forms.CharField(required=False)
    dni = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'placeholder': 'Nombre'})
        self.fields['apellido'].widget.attrs.update({'placeholder': 'Apellido'})
        self.fields['dni'].widget.attrs.update({'placeholder': 'DNI'})
    