# backend/apps/products/urls.py

from django.urls import path # type: ignore
from .views import (
    # CategoryListCreateView,
    # MyStoresDetailView,
    # MyStoreDetailView,
    # ProductListCreateView,
    CategoryDetailView,
    ProductDetailView
)

urlpatterns = [
    # path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories', CategoryDetailView.as_view(), name='categories-detail'),
    # path('mystore/', MyStoreDetailView.as_view(), name='mystore-detail'),
    path('details/', ProductDetailView.as_view(), name='product-detail'),
    # path('products/', ProductListCreateView.as_view(), name='product-list-create'),
]
