# backend/apps/store/urls.py

from rest_framework.routers import DefaultRouter
from django.urls import path, include # type: ignore
from .views import (
    # CategoryListCreateView,
    MyStoresDetailView,
    MyStoreDetailView,
    StoreCreateView,
    StoreView,
    StoreViewSet
    # ProductListCreateView,
)

router = DefaultRouter()
router.register(r'store', StoreViewSet, basename='store')

    # path('store', StoreViewSet),

urlpatterns = [
    path('', include(router.urls)),
    path('', StoreView.as_view(), name='store-view'),
    path('mystore/', MyStoreDetailView.as_view(), name='mystore-detail'),
    path('mystores', MyStoresDetailView.as_view(), name='mystores-detail'),
    path('create-store', StoreCreateView.as_view(), name='create-store'),
    # path('products/', ProductListCreateView.as_view(), name='product-list-create'),
]
