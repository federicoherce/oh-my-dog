# Generated by Django 4.1.7 on 2023-05-17 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('perros', '0002_libretasanitaria_alter_perro_fecha_de_nacimiento_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('hora', models.TimeField(default=django.utils.timezone.now)),
                ('cliente_asitio', models.BooleanField(default=False)),
                ('motivo', models.CharField(choices=[('Vacuna', 'Vacuna'), ('Vacuna antirrabica', 'Vacuna antirrabica'), ('Desparasitacion', 'Desparasitacion'), ('Castracion', 'Castracion'), ('Urgencia', 'Urgencia'), ('Consulta', 'Consulta')], max_length=20)),
                ('perro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perros.perro')),
                ('veterinario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]