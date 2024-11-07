from rest_framework import serializers # type: ignore
from .models import Product, Category
from backend.apps.categories.serializers import CategorySerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
