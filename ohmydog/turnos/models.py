from django.db import models
from django.utils import timezone
from autenticacion.models import CustomUser
from perros.models import Perro

# Create your models here.
class Turno(models.Model):
    MOTIVO_CHOICES = [
        ('Vacuna', 'Vacuna'),
        ('Vacuna antirrabica', 'Vacuna antirrabica'),
        ('Desparasitacion', 'Desparasitacion'),
        ('Castracion', 'Castracion'),
        ('Urgencia', 'Urgencia'),
        ('Consulta', 'Consulta')
    ]

    veterinario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(default=timezone.now)
    cliente_asitio = models.BooleanField(default=False)
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=20, choices=MOTIVO_CHOICES)
