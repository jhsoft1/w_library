# Generated by Django 4.0.2 on 2022-02-25 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0003_alter_book_options_bookinstance_borrower'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evening',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='EveningWhisky',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evening', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.evening')),
            ],
            options={
                'verbose_name_plural': 'EveningWhiskies',
            },
        ),
        migrations.CreateModel(
            name='Whisky',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Whiskies',
            },
        ),
        migrations.CreateModel(
            name='Tasting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nose', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='nose/Geruch (0-10)')),
                ('taste', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='taste/Geschmack (0-10)')),
                ('evening_whisky', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.eveningwhisky')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='eveningwhisky',
            name='whisky',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='catalog.whisky'),
        ),
        migrations.AddField(
            model_name='evening',
            name='whiskies',
            field=models.ManyToManyField(through='catalog.EveningWhisky', to='catalog.Whisky'),
        ),
        migrations.AddConstraint(
            model_name='tasting',
            constraint=models.UniqueConstraint(fields=('evening_whisky', 'user'), name='evening_whisky_user'),
        ),
        migrations.AddConstraint(
            model_name='tasting',
            constraint=models.CheckConstraint(check=models.Q(('nose__gte', 0), ('nose__lte', 10)), name='nose_between_0_10'),
        ),
        migrations.AddConstraint(
            model_name='tasting',
            constraint=models.CheckConstraint(check=models.Q(('taste__gte', 0), ('taste__lte', 10)), name='taste_between_0_10'),
        ),
        migrations.AddConstraint(
            model_name='eveningwhisky',
            constraint=models.UniqueConstraint(fields=('evening', 'whisky'), name='evening_whisky'),
        ),
    ]
