# Generated by Django 3.1.6 on 2021-03-09 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pix',
            old_name='img',
            new_name='src',
        ),
        migrations.AddField(
            model_name='pix',
            name='outlink',
            field=models.URLField(blank=True, null=True),
        ),
    ]
