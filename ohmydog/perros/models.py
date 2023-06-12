from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from autenticacion.models import CustomUser

# Create your models here.
class Perro(models.Model):
    RAZAS_PERRO = [
        ('labrador', 'Labrador'),
        ('bulldog', 'Bulldog'),
        ('pitbull', 'Pitbull'),
        ('boxer', 'Boxer'),
        ('pastor', 'Pastor aleman'),
        ('beagle', 'Beagle'),
        ('golden', 'Golden retriever'),
        ('fox', 'Fox Terrier'),
        ('esquimal', 'Esquimal canadiense'),
        ('dalmata', 'Dalmata'),
        ('yorkshire', 'Yorkshire terrier'),
        ('siberiano', 'Siberiano'),
        ('caniche', 'Caniche'),
        ('chihuahua', 'Chihuahua')
    ]

    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra')
    ]

    nombre = models.CharField(max_length=50)
    raza = models.CharField(max_length=50, choices=RAZAS_PERRO)
    color = models.CharField(max_length=50)
    fecha_de_nacimiento = models.DateField()
    dueño = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, default="")

    def __str__(self):
        return self.nombre
    
class LibretaSanitaria(models.Model):
    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, null=True)

class Vacuna(models.Model):
    tipo = models.CharField(max_length=50)
    fecha = models.DateField(default=timezone.now)
    libreta_sanitaria = models.ForeignKey(LibretaSanitaria, on_delete=models.CASCADE)
