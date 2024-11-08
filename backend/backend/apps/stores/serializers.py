# backend/apps/store/serializers.py

from rest_framework import serializers # type: ignore
from .models import Store
from backend.apps.products.serializers import ProductSerializer


class StoreSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Store
        fields = '__all__'

    def update(self, instance, validated_data):
        # print(instance._meta.fields)
        instance.store_name = validated_data.get('store_name', instance.store_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.store_description = validated_data.get('store_description', instance.store_description)
        instance.address = validated_data.get('address', instance.address)
        
        # instance.address
        return instance

