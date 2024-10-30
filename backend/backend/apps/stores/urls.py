# backend/apps/store/urls.py

from django.urls import path # type: ignore
from .views import (
    # CategoryListCreateView,
    MyStoresDetailView,
    MyStoreDetailView,
    # ProductListCreateView,
)

urlpatterns = [
    # path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('mystores', MyStoresDetailView.as_view(), name='mystores-detail'),
    path('mystore/', MyStoreDetailView.as_view(), name='mystore-detail'),
    # path('products/', ProductListCreateView.as_view(), name='product-list-create'),
]
