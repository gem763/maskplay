# Generated by Django 3.0.7 on 2020-11-15 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0014_auto_20201113_1625'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fashiontem',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('item', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='boo',
            name='fashiontem',
            field=models.ManyToManyField(blank=True, to='getch.Fashiontem'),
        ),
    ]