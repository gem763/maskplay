# Generated by Django 3.1.6 on 2021-10-17 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0097_researchitem_single_choice_only'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancegamerecord',
            name='pix_0',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pix_0_balancegamerecord_set', to='getch.pix'),
        ),
        migrations.AlterField(
            model_name='balancegamerecord',
            name='pix_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pix_1_balancegamerecord_set', to='getch.pix'),
        ),
    ]
