from django.shortcuts import render
from rest_framework import generics # type: ignore

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# Create your views here.
