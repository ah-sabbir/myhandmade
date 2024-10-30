from django.db import models
from django.db.models import JSONField
from django.conf import settings # type: ignore
from backend.apps.stores.models import Store


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class DocumentManager(models.Manager):
    def is_enable(self):
        return self.filter(is_enable=True)
        # super().queryset().filter()


def save_dir(instance, filename):
    print(instance.id)
    print(filename)
    return f'./static/images/product/{instance.id}-{filename}'


class Product(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rating = None

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to=save_dir)
    is_enable = models.BooleanField(default=True)
    objects = DocumentManager()
    properties = JSONField(default=dict)
    categories = models.ManyToManyField(Category, related_name="products")

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=("owner"), on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('product-detail', kwargs={'pk': self.pk})

    def rating(self):
        if self._rating is None:
            self._rating = ProductRating.objects.filter(
                product=self
            ).aggregate(
                avg_rating=Coalesce(models.Avg('rate'), 0),
                rating_count=models.Count('id')
            )
        return self._rating

    def rating_avg(self):
        return self.rating()['avg_rating']

    def rating_count(self):
        return self.rating()['rating_count']



# class Product(models.Model):
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='product_images/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=50)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)