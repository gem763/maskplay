# Generated by Django 3.0.7 on 2020-11-16 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0015_auto_20201116_0854'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boo',
            old_name='fashiontem',
            new_name='fashiontems',
        ),
    ]