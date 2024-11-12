from django.shortcuts import render
from rest_framework import generics # type: ignore
from rest_framework import status # type: ignore
from .models import Product, Category
from backend.apps.stores.models import Store
from rest_framework.permissions import IsAuthenticated # type: ignore
from .serializers import ProductSerializer, CategorySerializer, ProductImageSerializer
from rest_framework.views import APIView # type: ignore
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        queryset = Category.objects.all()
        categories = CategorySerializer(queryset, many=True)
        return Response({'categories':categories.data})


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        product = Store.objects.all()
        productserializer = ProductSerializer(product, many=True)
        return Response({'products':productserializer.data}, status=status.HTTP_200_OK)


# Product ViewSet with Complete CRUD Functionality
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

def create(self, request, *args, **kwargs):
        # Get the user's store
        try:
            store = Store.objects.get(owner=request.user)
        except Store.DoesNotExist:
            return Response({"error": "No store found for this user."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add owner and store to the request data
        data = request.data.copy()
        data.update({"owner": request.user.id, "store": store.id})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk, store__owner=request.user)
            serializer = self.get_serializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk, store__owner=request.user)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data.update({"owner": request.user.id, "store": product.store.id})

        serializer = self.get_serializer(product, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk, store__owner=request.user)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data.update({"owner": request.user.id, "store": product.store.id})

        serializer = self.get_serializer(product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk, store__owner=request.user)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        queryset = Product.objects.filter(store__owner=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
