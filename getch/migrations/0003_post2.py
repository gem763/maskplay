# Generated by Django 3.0.7 on 2020-08-19 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0002_auto_20200819_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post2',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('boo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='getch.Boo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
