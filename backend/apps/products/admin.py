from django.contrib import admin
from django.utils.html import mark_safe

from .models import (
    ProductImage,
    Product
    )

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_tag')  # Display product and the image thumbnail
    readonly_fields = ('image_tag',)  # Show thumbnail in the detail view

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
        return "No Image"

    image_tag.short_description = 'Image Preview'

