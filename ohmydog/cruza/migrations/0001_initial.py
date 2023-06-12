# Generated by Django 4.1.7 on 2023-06-06 18:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerroCruza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('raza', models.CharField(choices=[('labrador', 'Labrador'), ('bulldog', 'Bulldog'), ('pitbull', 'Pitbull'), ('boxer', 'Boxer'), ('pastor', 'Pastor aleman'), ('beagle', 'Beagle'), ('golden', 'Golden retriever'), ('fox', 'Fox Terrier'), ('esquimal', 'Esquimal canadiense'), ('dalmata', 'Dalmata'), ('yorkshire', 'Yorkshire terrier'), ('siberiano', 'Siberiano'), ('caniche', 'Caniche'), ('chihuahua', 'Chihuaha')], max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('fecha_de_nacimiento', models.DateField()),
                ('sexo', models.CharField(choices=[('macho', 'Macho'), ('hembra', 'Hembra')], max_length=10)),
                ('fecha_de_celo', models.DateField()),
                ('dueño', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]