# Generated by Django 4.2.2 on 2023-06-25 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_remove_userprofile_primo_accesso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='cognome',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='nome',
        ),
    ]