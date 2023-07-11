# Generated by Django 4.2.1 on 2023-07-07 04:05

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('paseadores_cuidadores', '0010_alter_paseadorcuidador_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Valoracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField(max_length=200)),
                ('puntaje', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('paseador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paseadores_cuidadores.paseadorcuidador')),
            ],
        ),
    ]
