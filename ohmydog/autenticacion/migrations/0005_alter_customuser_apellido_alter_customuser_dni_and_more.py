# Generated by Django 4.2 on 2023-05-12 21:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0004_alter_customuser_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='apellido',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[a-zA-Z]+$', 'El nombre solo debe contener caracteres.')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='dni',
            field=models.CharField(error_messages={'unique': 'Ya existe un usuario con este DNI'}, max_length=8, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]{8}$', 'El DNI debe tener 8 dígitos.')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nombre',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[a-zA-Z]+$', 'El nombre solo debe contener caracteres.')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='telefono',
            field=models.CharField(error_messages={'unique': 'Ya existe un usuario con este telefono'}, max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]+$', 'El teléfono solo debe contener números.')]),
        ),
    ]
