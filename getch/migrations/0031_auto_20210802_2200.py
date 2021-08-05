# Generated by Django 3.1.6 on 2021-08-02 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0030_auto_20210802_1844'),
    ]

    operations = [
        migrations.RenameField(
            model_name='researchitem',
            old_name='question',
            new_name='text',
        ),
        migrations.AlterField(
            model_name='researchitem',
            name='type',
            field=models.CharField(choices=[('AB', 'AB타입'), ('OX', 'OX타입'), ('QA', '주관식'), ('MC', '다중선택형'), ('IN', 'INTRO'), ('OUT', 'OUTRO')], default='AB', max_length=3),
        ),
    ]
