# Generated by Django 4.2.2 on 2023-06-26 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0014_alter_userprofile_favorite_movies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='favorite_movies',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='favorities',
            field=models.ManyToManyField(related_name='favorities', related_query_name='favorities', to='forum.movie'),
        ),
    ]