# Generated by Django 3.1.6 on 2021-03-17 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0011_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='pick',
            name='collection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='getch.collection'),
        ),
    ]
