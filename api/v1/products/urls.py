from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductDetailViewSet, SearchProductViewSet

app_name = "products"


router = DefaultRouter()
router.register(r'filter_products', ProductViewSet, basename='filter_products')
router.register(r'detail_products', ProductDetailViewSet, basename='detail_products')
router.register(r'search_products', SearchProductViewSet, basename='search_products')

urlpatterns = [
    path(r'', include(router.urls)),
]