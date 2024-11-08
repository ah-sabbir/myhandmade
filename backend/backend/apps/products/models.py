from django.db import models
from django.db.models import JSONField
from django.conf import settings # type: ignore
from backend.apps.stores.models import Store
from backend.apps.categories.models import Category

from django.db import models
from django.conf import settings
from django.db.models import JSONField, Sum, Count



class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DocumentManager(models.Manager):
    def is_enable(self):
        return self.filter(is_enable=True)


def save_dir(instance, filename):
    return f'./static/images/product/{instance.id}-{filename}'


class Product(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to=save_dir)
    is_enable = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    sku = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
    properties = JSONField(default=dict)  # Custom attributes
    categories = models.ManyToManyField(Category, related_name='product_category')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_store')
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=("owner"), on_delete=models.CASCADE, related_name='product_owner')

    objects = DocumentManager()

    def __str__(self):
        return self.name

    def average_rating(self):
        return self.rating_set.aggregate(avg_rating=Sum('rating'))['avg_rating'] or 0

    def rating_count(self):
        return self.rating_set.aggregate(count=Count('id'))['count'] or 0


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    variant_name = models.CharField(max_length=50)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"


class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Assuming rating scale from 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} - {self.rating}"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} wishlist - {self.product.name}"