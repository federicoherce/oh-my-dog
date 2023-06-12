from django.db import models
from autenticacion.models import CustomUser

# Create your models here.
class PerroCruza(models.Model):
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
        ('chihuahua', 'Chihuaha')
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
    fecha_de_celo = models.DateField()

    def __str__(self):
        return self.nombre