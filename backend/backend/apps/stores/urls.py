# backend/apps/store/urls.py

from django.urls import path # type: ignore
from .views import (
    # CategoryListCreateView,
    MyStoresDetailView,
    MyStoreDetailView,
    StoreCreateView,
    StoreView,
    # ProductListCreateView,
)

urlpatterns = [
    path('store', StoreView.as_view(), name='store-view'),
    path('mystore/', MyStoreDetailView.as_view(), name='mystore-detail'),
    path('mystores', MyStoresDetailView.as_view(), name='mystores-detail'),
    path('create-store', StoreCreateView.as_view(), name='create-store'),
    # path('products/', ProductListCreateView.as_view(), name='product-list-create'),
]
