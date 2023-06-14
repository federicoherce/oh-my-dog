from datetime import timezone
from xml.dom import ValidationErr
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator

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
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0, 'El monto a pagar debe ser mayor o igual a 0')])

