from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import RegexValidator

# Create your models here.
class PaseadorCuidador(models.Model):
    TIPO_CHOICES = [
        ('Paseador', 'Paseador'),
        ('Cuidador', 'Cuidador'),
    ]

    nomyap = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, default="")
    textolibre = models.TextField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='Paseador')

    
