# Generated by Django 4.2.2 on 2023-07-03 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0037_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.avatar'),
        ),
    ]
