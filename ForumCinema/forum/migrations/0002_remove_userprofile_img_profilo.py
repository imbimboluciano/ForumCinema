# Generated by Django 4.2.2 on 2023-06-22 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='img_profilo',
        ),
    ]
