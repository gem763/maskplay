# Generated by Django 3.0.7 on 2020-08-05 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0019_auto_20200805_1450'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mask',
            old_name='mask',
            new_name='maskbase',
        ),
    ]
