# backend/apps/store/admin.py

from django.contrib import admin
from .models import Category, Store#, Product

admin.site.register(Category)
admin.site.register(Store)
# admin.site.register(Product)
