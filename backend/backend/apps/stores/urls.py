# backend/apps/store/urls.py

from django.urls import path # type: ignore
from .views import (
    CategoryListCreateView,
    VendorDetailView,
    ProductListCreateView,
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('vendors/<str:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
]
