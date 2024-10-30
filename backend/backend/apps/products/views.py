from django.shortcuts import render
from rest_framework import generics # type: ignore
from rest_framework import status # type: ignore
from .models import Product, Category
from backend.apps.stores.models import Store
from rest_framework.permissions import IsAuthenticated # type: ignore
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.views import APIView # type: ignore
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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


# class ProductDetailView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return user.accounts.all()
        
#     def get(self, request):
#         user = request.user
#         # user_id = User.objects.get(email=user)
#         product = Store.objects.filter(user=user.id)
#         productserializer = ProductSerializer(product, many=True)
#         return Response({'products':productserializer.data}, status=status.HTTP_200_OK)

# Create your views here.
