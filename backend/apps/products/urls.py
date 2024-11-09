# backend/apps/products/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include # type: ignore
from .views import (
    # CategoryListCreateView,
    # MyStoresDetailView,
    # MyStoreDetailView,
    # ProductListCreateView,
    CategoryDetailView,
    ProductDetailView,
    ProductViewSet,
)

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]




    # path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    # path('categories', CategoryDetailView.as_view(), name='categories-detail'),
    # path('mystore/', MyStoreDetailView.as_view(), name='mystore-detail'),
    # path('details/', ProductDetailView.as_view(), name='product-detail'),
    # path('products/', ProductListCreateView.as_view(), name='product-list-create'),