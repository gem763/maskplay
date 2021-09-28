# Generated by Django 3.1.6 on 2021-09-28 18:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('getch', '0088_pix_tokens_ko'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.IntegerField(choices=[(0, '출첵게임'), (1, '매일밸런스게임'), (2, '옷장넣기'), (3, '리서치참여'), (4, '인터뷰참여'), (5, '첫방문환영'), (6, '기본정보입력'), (7, '관심스타일입력'), (8, '관심아이템입력'), (50, '테스트 INFLOW'), (100, '후원'), (101, '래플'), (102, '쇼핑')], default=0),
        ),
        migrations.CreateModel(
            name='Notihistory',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('slacked', models.BooleanField(default=False)),
                ('mobiled', models.BooleanField(default=False)),
                ('emailed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='getch.transaction')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
