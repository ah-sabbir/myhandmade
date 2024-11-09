from django.contrib import admin
from .models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)

# class ProductAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}
