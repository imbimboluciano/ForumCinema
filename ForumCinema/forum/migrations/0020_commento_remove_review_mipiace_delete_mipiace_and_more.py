# Generated by Django 4.2.2 on 2023-06-26 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0019_mipiace_alter_review_mipiace'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrizione', models.CharField(max_length=250)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='review',
            name='mipiace',
        ),
        migrations.DeleteModel(
            name='Mipiace',
        ),
        migrations.AddField(
            model_name='review',
            name='commenti',
            field=models.ManyToManyField(related_name='commenti', to='forum.commento'),
        ),
    ]
