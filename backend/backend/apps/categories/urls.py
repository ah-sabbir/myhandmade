from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet#, ProductViewSet

# router = DefaultRouter()
# router.register(r'categories', CategoryViewSet)
# router.register(r'products', ProductViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]


urlpatterns = [
    path('', CategoryViewSet, name='get-products-by-category'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('category', CategoryDetailView.as_view(), name='categories-detail'),
]