# Generated by Django 3.0.7 on 2020-09-02 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0008_boo_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='boo',
            name='nposts',
            field=models.IntegerField(default=0),
        ),
    ]
