from django.db import models
from django.db.models import JSONField
from django.conf import settings # type: ignore
from backend.apps.stores.models import Store
# from backend.apps.categories.models import Category

from django.db import models
from django.conf import settings
from django.db.models import JSONField, Sum, Count


import urllib.request
from urllib.error import HTTPError
from django.core.files import File
from io import BytesIO
import uuid
from datetime import datetime


class DocumentManager(models.Manager):
    def is_enable(self):
        return self.filter(is_enable=True)


def save_dir(instance, filename):
    return f'./static/images/product/{instance.id}-{filename}'


class Product(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=False, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    images = models.ManyToManyField('ProductImage', related_name='product_images')
    is_enable = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    sku = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
    properties = JSONField(default=dict)  # Custom attributes
    categories = models.ManyToManyField('Category', related_name='products')

    # brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_store')
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=("owner"), on_delete=models.CASCADE, related_name='product_owner')

    objects = DocumentManager()

    def __str__(self):
        return self.name

    def average_rating(self):
        return self.rating_set.aggregate(avg_rating=Sum('rating'))['avg_rating'] or 0

    def rating_count(self):
        return self.rating_set.aggregate(count=Count('id'))['count'] or 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to=save_dir, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image_url and not self.image:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
            filename = f"{timestamp}_{uuid.uuid4()}.jpg"
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                req = urllib.request.Request(self.image_url, headers=headers)
                with urllib.request.urlopen(req) as response:
                    image_data = response.read()
                    image_file = BytesIO(image_data)
                    self.image.save(f"{filename}.jpg", File(image_file), save=False)
            except HTTPError as e:
                print(f"Failed to fetch image: {e}")
        super().save(*args, **kwargs)


class Brand(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_brand')
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variants')
    variant_name = models.CharField(max_length=50)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"


class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Assuming rating scale from 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} - {self.rating}"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_wishlists')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} wishlist - {self.product.name}"


from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name