# Generated by Django 3.0.7 on 2020-07-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0005_auto_20200630_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='boo_id',
            field=models.IntegerField(default=0),
        ),
    ]
