# Generated by Django 3.1.6 on 2021-06-22 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0006_auto_20210615_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='boo',
            name='coltagged',
            field=models.BooleanField(default=False),
        ),
    ]