# Generated by Django 4.2.2 on 2023-06-24 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_movie_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='regista',
        ),
        migrations.AlterField(
            model_name='movie',
            name='anno',
            field=models.CharField(max_length=200),
        ),
    ]
