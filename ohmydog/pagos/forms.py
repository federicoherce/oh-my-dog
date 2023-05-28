from time import timezone
from xml.dom import ValidationErr
from django import forms
from datetime import date
from .models import Tarjeta, Pago
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

def validate_fecha_vencimiento(value):
    if value <= timezone.now().date():
        raise ValidationErr("La fecha de vencimiento debe ser posterior a la fecha actual.")

class CrearTarjeta(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ('numeroTarjeta', 'nombreTitular', 'fechaVencimiento', 'codigoSeguridad',)


class CrearPago(forms.ModelForm):
    class Meta:
        model = Pago 
        fields = ('monto', 'turno')



