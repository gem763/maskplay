# Generated by Django 3.1.6 on 2021-03-17 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0015_auto_20210317_2339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('name', models.TextField(default='옷장이름', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='getch.boo')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='getch.collection')),
                ('pix', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getch.pix')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
    ]
