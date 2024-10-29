from django.db import models
from backend.apps.stores.models import Category

class DocumentManager(models.Manager):
    def is_enable(self):
        return self.filter(is_enable=True)
        # super().queryset().filter()


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
    categurise = models.ManyToManyField(Category, related_name="products")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        old_image = ''
        if self.image:
            old_image = self.image
            self.image = ''
            super().save(*args, **kwargs)
        self.image = old_image
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if not "Mapsa" in self.name:
            raise ValidationError("Must include Mapsa")

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})

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



class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant_name = models.CharField(max_length=50)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2)
