from django.db import models
from django.core.validators import RegexValidator
from autenticacion.models import CustomUser


# Create your models here.
class Adopcion(models.Model):
    TAMAÑO_CHOICES = [
        ('P', 'Pequeño'),
        ('M', 'Mediano'),
        ('G', 'Grande'),
    ]

    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
    ]
    
    SOLO_CARACTERES = RegexValidator(r'^[a-zA-Z\sáÁéÉíÍóÓúÚ]+$', 'Este campo solo puede contener caracteres.')
    
    publicado_por = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    nombre = models.CharField(max_length=30, validators=[SOLO_CARACTERES])
    raza = models.CharField(max_length=30, validators=[SOLO_CARACTERES])
    color = models.CharField(max_length=30, validators=[SOLO_CARACTERES])
    tamaño = models.CharField(max_length=10, choices=TAMAÑO_CHOICES)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    origen = models.CharField(max_length=30, validators=[SOLO_CARACTERES])
    observacion = models.CharField(blank=True, max_length=100)
    adoptado = models.BooleanField(default=False)
    