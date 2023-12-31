# Generated by Django 4.2.2 on 2023-06-25 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_movie_poster_alter_userprofile_citazione'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='favorite_movies',
            field=models.ManyToManyField(to='forum.movie'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='citazione',
            field=models.ForeignKey(default=17, on_delete=django.db.models.deletion.CASCADE, to='forum.citazione'),
        ),
    ]
