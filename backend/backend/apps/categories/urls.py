from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CategoryListCreateView, CategoryDetailView#, ProductViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('category/', CategoryListCreateView.as_view(), name='category-list-create'),
    # path('', CategoryDetailView.as_view(), name='categories-detail'),
]