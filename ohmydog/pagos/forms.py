from time import timezone
from xml.dom import ValidationErr
from django import forms
from datetime import date
from .models import Pago
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

def validate_fecha_vencimiento(value):
    current_month = date.today().month
    current_year = date.today().year

    # Verificar si la fecha de vencimiento tiene el formato correcto "MM/YYYY"
    if len(value) != 7 or value[2] != '/':
        raise forms.ValidationError("Ingrese la fecha de vencimiento en el formato MM/YYYY.")

    expiration_month, expiration_year = value[:2], value[3:]

    if not expiration_month.isdigit() or not expiration_year.isdigit():
        raise forms.ValidationError("El formato de la fecha de vencimiento debe contener solo dígitos para MM y AAAA.")

    if int(expiration_year) < current_year:
        raise forms.ValidationError("La fecha de vencimiento debe ser posterior a la fecha actual.")

    if int(expiration_year) == current_year and expiration_month < current_month:
        raise forms.ValidationError("La fecha de vencimiento debe ser posterior a la fecha actual.")


class TarjetaForm(forms.Form):
    SOLO_CARACTERES = RegexValidator(r'^[a-zA-Z\sáÁéÉíÍóÓúÚ]+$', 'Este campo solo puede contener caracteres.')
    numero_tarjeta = forms.CharField(label='Número de Tarjeta', max_length=16, required=True, validators=[
            RegexValidator(r'^[0-9]{16}$', 'El numero de tarjeta debe ser de 16 dígitos.')])
    fecha_vencimiento = forms.CharField(label='Fecha de Vencimiento (MM/YYYY)', max_length=7, required=True, validators=[validate_fecha_vencimiento])
    nombre_titular = forms.CharField(label='Nombre del Titular', max_length=100, required=True, validators=[SOLO_CARACTERES])
    codigo_seguridad = forms.CharField(label='Código de Seguridad', max_length=3, required=True, validators=[
            RegexValidator(r'^[0-9]{3}$', 'El código debe ser de 3 dígitos.')])


class CrearPago(forms.ModelForm):
    class Meta:
        model = Pago 
        fields = ('monto',)



