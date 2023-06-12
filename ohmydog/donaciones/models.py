from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from autenticacion.models import CustomUser

class Donacion(models.Model):
    monto = models.CharField(max_length=10)


class Campaña(models.Model):
    nombre = models.CharField(max_length=30)
    monto_objetivo = models.DecimalField(max_digits=2)
    descripcion = CharField = models.CharField(max_length=200)
