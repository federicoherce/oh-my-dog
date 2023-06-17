from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from autenticacion.models import CustomUser

class Donacion(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nombre = models.CharField(max_length=30, blank=True, default="")
    tipo = models.CharField(max_length=12)
    fecha = models.DateField(default=timezone.now)


class Campaña(models.Model):
    nombre = models.CharField(max_length=30, unique=True, error_messages={
            'unique': 'Ya existe una campaña con este email'})
    monto_objetivo = models.DecimalField(decimal_places=2, max_digits=12)
    descripcion = models.TextField(max_length=200)
