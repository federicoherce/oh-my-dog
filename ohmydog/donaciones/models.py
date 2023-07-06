from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from autenticacion.models import CustomUser



class Campaña(models.Model):
    nombre = models.CharField(max_length=30, unique=True, error_messages={
            'unique': 'Ya existe un usuario con este email'})
    monto_objetivo = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(1)])
    descripcion = models.TextField(max_length=200)
    finalizada = models.BooleanField(default=False)

class Donacion(models.Model):
    TIPO_CHOICES = [
        ('Campaña', 'Campaña'),
        ('Veterinaria', 'Veterinaria'),
    ]

    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    nombre = models.CharField(max_length=30, blank=True, default="")
    fecha = models.DateField(default=timezone.now)
    tipo = models.CharField(max_length=12, choices=TIPO_CHOICES)
    campana = models.ForeignKey(Campaña, null=True, blank="", on_delete=models.CASCADE)
    motivo = models.TextField(max_length=200, default='')

