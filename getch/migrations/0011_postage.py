# Generated by Django 3.1.6 on 2021-06-25 20:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import getch.models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0010_auto_20210625_1925'),
    ]

    operations = [
        migrations.CreateModel(
            name='Postage',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('pix_a', models.ImageField(max_length=500, upload_to=getch.models._postagepix_path)),
                ('pix_b', models.ImageField(max_length=500, upload_to=getch.models._postagepix_path)),
                ('pixlabel_a', models.TextField(blank=True, max_length=200, null=True)),
                ('pixlabel_b', models.TextField(blank=True, max_length=200, null=True)),
                ('group', models.CharField(max_length=30)),
                ('contentwork', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='getch.contentwork')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]