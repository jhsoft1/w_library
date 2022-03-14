# Generated by Django 4.0.3 on 2022-03-14 09:25

import catalog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_alter_tasting_taste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whisky',
            name='name',
            field=models.CharField(max_length=128, primary_key=True, serialize=False, validators=[catalog.models.validate_no_slash]),
        ),
    ]
