# backend/apps/store/views.py

from rest_framework import generics # type: ignore
from .models import Category, Vendor, Product
from .serializers import CategorySerializer, VendorSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated # type: ignore

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.vendor)  # Assumes user has a related vendor
