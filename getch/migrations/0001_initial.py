# Generated by Django 3.0.7 on 2020-08-10 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import getch.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('boo_selected', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MaskBase',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('EYE', 'eye'), ('MOUTH', 'mouth')], default='EYE', max_length=5)),
                ('category', models.CharField(default='base', max_length=50)),
                ('pix', models.ImageField(max_length=500, upload_to=getch.models._maskpix_path)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('IMAGE', 'image'), ('TEXT', 'text')], default='IMAGE', max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mask',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('top', models.FloatField(default=0)),
                ('left', models.FloatField(default=0)),
                ('width', models.FloatField(default=100)),
                ('height', models.FloatField(default=20)),
                ('maskbase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='getch.MaskBase')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Flager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, verbose_name='Note')),
                ('status', models.IntegerField(blank=True, db_index=True, null=True, verbose_name='Status')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('object_id', models.PositiveIntegerField(db_index=True, verbose_name='Object ID')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='getch_flager_flags', to='contenttypes.ContentType', verbose_name='Content type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flager_users', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Flag',
                'verbose_name_plural': 'Flags',
                'abstract': False,
                'unique_together': {('content_type', 'object_id', 'user', 'status')},
            },
        ),
    ]
