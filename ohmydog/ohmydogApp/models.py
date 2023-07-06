from django.db import models

# Create your models here.
class RedSocial(models.Model):
    TIPO_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instragram'),
        ('reddit', 'Reddit'),
        ('')
    ]

class Veterinaria(models.Model):
    nombre = models.CharField(max_length=50)
    calle = models.CharField(max_length=50)
    nro_calle = models.IntegerField()
    detalle = models.TextField(max_length=500, blank=True, null=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.latitud} {self.longitud}"