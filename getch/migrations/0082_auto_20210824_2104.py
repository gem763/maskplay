# Generated by Django 3.1.6 on 2021-08-24 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0081_auto_20210824_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashgametag',
            name='answer',
            field=models.JSONField(blank=True, default=list, max_length=20, null=True),
        ),
    ]
