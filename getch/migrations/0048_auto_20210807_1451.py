# Generated by Django 3.1.6 on 2021-08-07 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0047_remove_shoptem_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoptem',
            name='item',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='getch.item'),
        ),
    ]
