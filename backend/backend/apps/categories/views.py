from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Category
from .serializers import CategorySerializer
from backend.apps.products.models import Product  # Adjust the import based on your project structure
from backend.apps.products.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.permissions import AllowAny
from rest_framework import generics # type: ignore
from rest_framework import status # type: ignore

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response({'categories':serializer.data})

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):  # Use ReadOnlyModelViewSet for GET-only functionality
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'], url_path='products')  # Custom action to get products by category
    def get_products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(categories=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.prefetch_related('subcategories')