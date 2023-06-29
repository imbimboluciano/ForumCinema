# Generated by Django 4.2.2 on 2023-06-29 14:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0029_cinemaclub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinemaclub',
            name='members',
            field=models.ManyToManyField(related_name='members', related_query_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
