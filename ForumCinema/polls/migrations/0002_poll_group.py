# Generated by Django 4.2.2 on 2023-06-30 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0034_remove_poll_group_remove_poll_owner_and_more'),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='group',
            field=models.ForeignKey(default=9, on_delete=django.db.models.deletion.CASCADE, to='forum.cinemaclub'),
        ),
    ]