from django.db import models

class Perdidos(models.Model):
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
    
    TAMAÑO_CHOICES = [
        ('Pequeño', 'Pequeño'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
    ]
    
    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ]
    
    ESTADO_CHOICES = [
        ('Busco a su dueño', 'Busco a su dueño'),
        ('Perdi a mi perro', 'Perdi a mi perro'),
    ]
    
     
    nombre = models.CharField(max_length=50)
    raza = models.CharField(max_length=50, choices=RAZAS_PERRO)
    color = models.CharField(max_length=50)
    tamaño = models.CharField(max_length=10, choices=TAMAÑO_CHOICES)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    origen = models.CharField(max_length=50)
    observacion = models.CharField(blank=True, max_length=100)
    estado = models.CharField(max_length=25, choices=ESTADO_CHOICES)
    imagen = models.ImageField(upload_to='perdidos/')
    telefono = models.CharField(max_length=25, default="1")
    encontrado = models.BooleanField(default=False)
    
    
    

# Create your models here.
