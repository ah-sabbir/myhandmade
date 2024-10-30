# Generated by Django 5.1.2 on 2024-10-30 04:39

import backend.apps.stores.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.RemoveField(
            model_name='product',
            name='vendor',
        ),
        migrations.RemoveField(
            model_name='productvariant',
            name='product',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='user',
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('store_name', models.CharField(max_length=50)),
                ('store_description', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=backend.apps.stores.models.save_dir)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_enable', models.BooleanField(default=True)),
                ('phone_number', models.BigIntegerField(unique=True)),
                ('address', models.TextField(blank=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='ProductVariant',
        ),
        migrations.DeleteModel(
            name='Vendor',
        ),
    ]