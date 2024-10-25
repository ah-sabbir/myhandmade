# backend/apps/store/views.py
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

from rest_framework import generics # type: ignore
from .models import Category, Vendor, Product
from .serializers import CategorySerializer, VendorSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticated # type: ignore

import uuid

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


# for multiple store view
class MyStoresDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # user_id = User.objects.get(email=user)
        vendor = Vendor.objects.filter(user=user.id)
        mystore = VendorSerializer(vendor, many=True)
        return Response({'mystore':mystore.data}, status=status.HTTP_200_OK)

# for single store view
class MyStoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def is_valid_uuid(self, uuid_string):
        try:
            uuid_obj = uuid.UUID(uuid_string, version=4)  # You can specify the version you want
        except ValueError:
            return False
        return str(uuid_obj) == uuid_string

    def get(self, request):
        try:
            store_id = request.GET.get('store_id')
            if store_id and self.is_valid_uuid(store_id):
                user = request.user
                # user_id = User.objects.get(email=user)
                vendor = Vendor.objects.filter(user=user.id, id=store_id)
                mystore = VendorSerializer(vendor, many=True)
                return Response({'mystore':mystore.data}, status=status.HTTP_200_OK)
            
            return Response({'error':'store_id is required or value error'}, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response({'error':'Something went wrong or there is no store created'}, status=status.HTTP_400_BAD_REQUEST)


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.vendor)  # Assumes user has a related vendor
