# Generated by Django 3.0.7 on 2021-02-02 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0009_auto_20210131_0456'),
    ]

    operations = [
        migrations.AddField(
            model_name='boo',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
