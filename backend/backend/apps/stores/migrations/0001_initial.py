# Generated by Django 5.1.2 on 2024-11-08 04:50

import backend.apps.stores.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('store_name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=50, unique=True)),
                ('store_description', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=backend.apps.stores.models.save_dir)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_enable', models.BooleanField(default=True)),
                ('phone_number', models.BigIntegerField(unique=True)),
                ('address', models.TextField(blank=True)),
            ],
        ),
    ]
