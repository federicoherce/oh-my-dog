# Generated by Django 4.2 on 2023-06-05 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paseadores_cuidadores', '0008_alter_paseadorcuidador_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paseadorcuidador',
            name='email',
            field=models.EmailField(default='', error_messages={'unique': 'Ya existe un paseador o cuidador con este email'}, max_length=50, unique=True),
        ),
    ]
