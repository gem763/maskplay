# Generated by Django 3.1.6 on 2021-08-05 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0033_auto_20210803_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='boo',
            name='answers',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]