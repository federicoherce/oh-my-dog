from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import RegexValidator

# Create your models here.
class PaseadorCuidador(models.Model):
    TIPO_CHOICES = [
        ('P', 'Paseador'),
        ('C', 'Cuidador'),
    ]

    nomyap = models.CharField(max_length=50)
    dni = models.CharField(unique=True, error_messages={'unique': 'Ya existe un usuario con este DNI'}, max_length=8, validators=[
            RegexValidator(r'^[0-9]{8}$', 'El DNI debe tener 8 dígitos.')])
    textolibre = models.TextField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='P')

    
