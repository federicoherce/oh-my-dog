from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from autenticacion.models import CustomUser

# Create your models here.
class Perro(models.Model):
    nombre = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    fecha_de_nacimiento = models.DateField()
    dueño = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
class LibretaSanitaria(models.Model):
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE)

class Vacuna(models.Model):
    tipo = models.CharField(max_length=50)
    fecha = models.DateField(default=timezone.now)
    libreta_sanitaria = models.ForeignKey(LibretaSanitaria, on_delete=models.CASCADE)
