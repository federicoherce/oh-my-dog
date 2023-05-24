from django import forms
from django.db import models 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from datetime import date


SOLO_CARACTERES = RegexValidator(r'^[a-zA-Z\sáÁéÉíÍóÓúÚ]+$', 'Este campo solo puede contener caracteres.')

class CustomUserCreationForm(UserCreationForm):    
    class Meta:
        model = CustomUser
        fields = ('email', 'nombre', 'apellido', 'dni', 'telefono',)
        
        
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Email"),
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
    
class CambiarEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
            attrs={'placeholder': 'Escriba su nueva dirección de correo electrónico'}))
    

class modificarDatosCliente(forms.Form):
    nombre = forms.CharField(max_length=30, required=True, validators=[SOLO_CARACTERES])
    apellido = forms.CharField(max_length=30, required=True, validators=[SOLO_CARACTERES])
    dni = forms.CharField(max_length=8, required=True, validators=[
            RegexValidator(r'^[0-9]{8}$', 'El DNI debe tener 8 dígitos.')], error_messages= {
            'unique': 'Ya existe un usuario con este DNI'})
    telefono = forms.CharField(max_length=15, required=True, validators=[
            RegexValidator(r'^[0-9]+$', 'El teléfono solo debe contener números.')], error_messages={
            'unique': 'Ya existe un usuario con este telefono'})
    
# forms.Form => Se usa cuando se quiere crear un formulario independiente, desde cero. Hay que definir manualmente 
# los campos y las validaciones para el formulario.
# forms.ModelForm => Se usa cuando se quiere crear un formulario basado en un modelo existente. Los campos y 
# las validaciones se generan automáticamente según el modelo.

class ModificarDatosPerro(forms.Form):
    nombre = forms.CharField(max_length=50)
    raza = forms.CharField(max_length=50)
    color = forms.CharField(max_length=50)
    fecha_de_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.widgets.DateInput(attrs={'type': 'date', 'max': str(date.today())}),
        input_formats=['%Y-%m-%d']
    )
    