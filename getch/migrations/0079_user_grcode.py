# Generated by Django 3.1.6 on 2021-08-23 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0078_auto_20210818_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='grcode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]