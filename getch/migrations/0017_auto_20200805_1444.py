# Generated by Django 3.0.7 on 2020-08-05 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0016_auto_20200805_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='eye_mask',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='mouth_mask',
        ),
    ]
