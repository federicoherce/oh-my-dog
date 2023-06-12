from django.db import models
from autenticacion.models import CustomUser
from perros.models import Perro

# Create your models here.
class PerroCruza(models.Model):
    dueño = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE)
    fecha_de_celo = models.DateField()

