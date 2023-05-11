from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.
class PaseadorCuidador(models.Model):
    nomyap = models.CharField(max_length=50)
    dni = models.CharField(error_messages={'unique': 'Ya existe un usuario con este DNI'}, max_length=30, unique=True)
    textolibre = models.TextField(max_length=200)
    
