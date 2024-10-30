# backend/apps/store/models.py

from django.db import models # type: ignore
from django.conf import settings # type: ignore
import uuid
# from backend.apps.products.models import Product


def save_dir(instance, filename):
    print(instance.id)
    print(filename)
    return f'./static/images/store/{instance.id}-{filename}'


class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Primary key
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=("owner"), on_delete=models.CASCADE, related_name='stores')
    store_name = models.CharField(max_length=50)
    store_description = models.TextField(blank=True)
    logo = models.ImageField(upload_to=save_dir, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_enable = models.BooleanField(default=True)
    phone_number = models.BigIntegerField(unique=True)
    address = models.TextField(blank=True)

    # products = models.ManyToManyField(Product, related_name='stores')
    # products = models.ManyToManyField(Product, related_name='stores')

    def __str__(self):
        return self.store_name

