from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from autenticacion.models import CustomUser

class Donacion(models.Model):
    monto = models.CharField(max_length=10)


class Campaña(models.Model):
    nombre = models.CharField(max_length=30, unique=True, error_messages={
            'unique': 'Ya existe un usuario con este email'})
    monto_objetivo = models.DecimalField(decimal_places=2, max_digits=12)
    descripcion = models.CharField(max_length=200)
