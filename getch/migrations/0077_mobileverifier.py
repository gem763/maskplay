# Generated by Django 3.1.6 on 2021-08-18 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0076_user_mobile_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobileVerifier',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('mobile', models.CharField(max_length=20)),
                ('authkey', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
