# Generated by Django 4.2.2 on 2023-06-25 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_alter_userprofile_citazione'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='primo_accesso',
            field=models.BooleanField(default=False),
        ),
    ]