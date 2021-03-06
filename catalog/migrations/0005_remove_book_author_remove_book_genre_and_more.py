# Generated by Django 4.0.3 on 2022-03-09 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_evening_eveningwhisky_whisky_tasting_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='book',
            name='language',
        ),
        migrations.RemoveField(
            model_name='bookinstance',
            name='book',
        ),
        migrations.RemoveField(
            model_name='bookinstance',
            name='borrower',
        ),
        migrations.AlterModelOptions(
            name='whisky',
            options={'ordering': ['name'], 'verbose_name_plural': 'Whiskies'},
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='BookInstance',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
    ]
