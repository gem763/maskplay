# Generated by Django 3.1.6 on 2021-10-08 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0095_raffle_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='raffle',
            name='send_requested',
            field=models.BooleanField(default=False),
        ),
    ]
