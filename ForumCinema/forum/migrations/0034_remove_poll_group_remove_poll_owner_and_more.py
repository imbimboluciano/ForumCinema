# Generated by Django 4.2.2 on 2023-06-30 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0033_choice_poll_vote_remove_question_creator_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='group',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='poll',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Poll',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
