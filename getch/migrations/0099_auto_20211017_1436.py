# Generated by Django 3.1.6 on 2021-10-17 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0098_auto_20211017_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='balancegamerecord',
            name='tag_0',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tag_0_balancegamerecord_set', to='getch.tag'),
        ),
        migrations.AddField(
            model_name='balancegamerecord',
            name='tag_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tag_1_balancegamerecord_set', to='getch.tag'),
        ),
    ]
