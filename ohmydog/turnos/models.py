from django.db import models
from django.utils import timezone
from autenticacion.models import CustomUser
from perros.models import Perro

# Create your models here.
class Turno(models.Model):
    MOTIVO_CHOICES = [
        ('vacuna', 'Vacuna'),
        ('vacuna_antirrabica', 'Vacuna antirrabica'),
        ('desparasitacion', 'Desparasitación'),
        ('castracion', 'Castración'),
        ('urgencia', 'Urgencia'),
        ('consulta', 'Consulta general')
    ]
    HORARIO_CHOICES = [
        ('tarde', 'Tarde'),
        ('mañana', 'Mañana')
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
        ('modificado', 'Modificado')
    ]

    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.CharField(max_length=20, choices=HORARIO_CHOICES)
    cliente_asistio = models.BooleanField(default=False, null=True)
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=20, choices=MOTIVO_CHOICES)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
