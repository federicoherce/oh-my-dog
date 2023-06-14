# Generated by Django 4.2.1 on 2023-06-14 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donaciones', '0002_donacion_nombre_alter_campaña_descripcion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='donacion',
            name='tipo',
            field=models.CharField(choices=[('Campaña', 'Campaña'), ('Veterinaria', 'Veterinaria')], default='Campaña', max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donacion',
            name='nombre',
            field=models.CharField(blank=True, default='Zz', max_length=30),
        ),
    ]
