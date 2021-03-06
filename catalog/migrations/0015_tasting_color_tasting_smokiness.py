# Generated by Django 4.0.3 on 2022-03-14 11:00

import catalog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_alter_whisky_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasting',
            name='color',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True, validators=[catalog.models.validate_empty_or_0_10], verbose_name='color/Farbe (0-10)'),
        ),
        migrations.AddField(
            model_name='tasting',
            name='smokiness',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True, validators=[catalog.models.validate_empty_or_0_10], verbose_name='smokiness/Rauchigkeit (0-10)'),
        ),
    ]
