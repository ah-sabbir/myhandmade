# backend/apps/store/admin.py

from django.contrib import admin
from .models import Category, Vendor, Product

admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Product)
