# Generated by Django 5.1.2 on 2024-11-09 17:55

import backend.apps.users.models
import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('state_code', models.CharField(max_length=5)),
                ('postal_code', models.CharField(max_length=20)),
                ('coordinates', models.JSONField()),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='Unknown', max_length=150)),
                ('last_name', models.CharField(default='Unknown', max_length=150)),
                ('age', models.IntegerField(blank=True, editable=False, null=True)),
                ('gender', models.CharField(choices=[('Female', 'female'), ('Male', 'male'), ('Other', 'other')], default='customer', max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$')])),
                ('birthDate', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=backend.apps.users.models.save_dir)),
                ('phone_verified', models.BooleanField(default=False)),
                ('user_type', models.CharField(choices=[('vendor', 'vendor'), ('customer', 'customer'), ('seller', 'seller')], default='customer', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_pro', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.address')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
