from django.db.models import Avg
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from autenticacion.models import CustomUser
from star_ratings.models import *

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
    def calcular_promedio_puntaje(self):
        return self.valoracion_set.aggregate(promedio=Avg('puntaje'))['promedio']
    def ha_realizado_valoracion(self, request):
        return Valoracion.objects.filter(paseador=self, cliente=request.user).exists()

class Valoracion(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    paseador = models.ForeignKey(PaseadorCuidador, on_delete=models.CASCADE)
    comentario = models.TextField(max_length=200, blank=True)
    puntaje = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ])
    


