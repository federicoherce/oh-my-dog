# Generated by Django 4.2.1 on 2023-07-11 21:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paseadores_cuidadores', '0014_alter_valoracion_unique_together_valoracion_puntaje_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valoracion',
            name='comentario',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='valoracion',
            name='puntaje',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
