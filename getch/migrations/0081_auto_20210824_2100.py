# Generated by Django 3.1.6 on 2021-08-24 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0080_flashgametag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashgametag',
            name='answer',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]