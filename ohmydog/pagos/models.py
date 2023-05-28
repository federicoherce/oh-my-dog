from datetime import timezone
from xml.dom import ValidationErr
from django.db import models
from django.core.validators import RegexValidator
from turnos.models import Turno

def validate_fecha_vencimiento(value):
    current_month = timezone.now().strftime('%m')
    current_year = timezone.now().strftime('%Y')

    # Verificar si la fecha de vencimiento tiene el formato correcto "MM/YYYY"
    if len(value) != 7 or value[2] != '/':
        raise ValidationErr("Ingrese la fecha de vencimiento en el formato MM/YYYY.")

    expiration_month, expiration_year = value[:2], value[3:]

    if expiration_year < current_year:
        raise ValidationErr("La fecha de vencimiento debe ser posterior a la fecha actual.")

    if expiration_year == current_year and expiration_month < current_month:
        raise ValidationErr("La fecha de vencimiento debe ser posterior a la fecha actual.")


# Create your models here.
class Pago(models.Model):    
    SOLO_CARACTERES = RegexValidator(r'^[a-zA-Z\sáÁéÉíÍóÓúÚ]+$', 'Este campo solo puede contener caracteres.')
    
    monto = models.DecimalField(max_digits=10, decimal_places=2)


class Tarjeta(models.Model):
    SOLO_CARACTERES = RegexValidator(r'^[a-zA-Z\sáÁéÉíÍóÓúÚ]+$', 'Este campo solo puede contener caracteres.')

    numeroTarjeta = models.CharField(max_length=16, validators=[
            RegexValidator(r'^[0-9]{16}$', 'El numero de tarjeta debe tener maximo 16 caracteres')])
    nombreTitular = models.CharField(max_length=40, validators=[SOLO_CARACTERES])
    fechaVencimiento = models.DateField(max_length=7, validators=[validate_fecha_vencimiento])
    codigoSeguridad = models.CharField(max_length=4, validators=[
            RegexValidator(r'^[0-9]{4}$', 'El codigo de seguridad debe tener maximo 4 caracteres')])