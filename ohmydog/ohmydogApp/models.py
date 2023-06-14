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