# backend/apps/store/serializers.py

from rest_framework import serializers # type: ignore
from .models import Store


class StoreSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    class Meta:
        model = Store
        fields = '__all__'

