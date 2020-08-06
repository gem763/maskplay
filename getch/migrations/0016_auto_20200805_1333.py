# Generated by Django 3.0.7 on 2020-08-05 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0015_auto_20200805_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='maskbase',
            name='category',
            field=models.CharField(default='base', max_length=50),
        ),
        migrations.AlterField(
            model_name='maskbase',
            name='type',
            field=models.CharField(choices=[('EYE', 'eye'), ('MOUTH', 'mouth')], default='EYE', max_length=5),
        ),
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.CharField(choices=[('PIX', 'pix'), ('TXT', 'txt')], default='PIX', max_length=5),
        ),
    ]