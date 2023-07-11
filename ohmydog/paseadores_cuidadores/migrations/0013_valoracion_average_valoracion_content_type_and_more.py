# Generated by Django 4.2.1 on 2023-07-09 03:03

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('paseadores_cuidadores', '0012_remove_valoracion_puntaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='valoracion',
            name='average',
            field=models.DecimalField(decimal_places=3, default=Decimal('0'), max_digits=6),
        ),
        migrations.AddField(
            model_name='valoracion',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='valoracion',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='valoracion',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='valoracion',
            name='total',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='valoracion',
            unique_together={('content_type', 'object_id')},
        ),
    ]
