# Generated by Django 4.2.2 on 2023-07-02 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0035_review_date_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date_published',
            field=models.DateField(),
        ),
    ]
