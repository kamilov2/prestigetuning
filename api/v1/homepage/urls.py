from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerViewSet, CategoryViewSet, TopSellingProductsView, RecommendedProductsView, ContactAPIView
router = DefaultRouter()
router.register(r'banners', BannerViewSet, basename='banners')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'topsellingproducts', TopSellingProductsView, basename='topsellingproducts')
router.register(r'recommendedproducts', RecommendedProductsView, basename='recommendedproducts')


urlpatterns = [
    path('', include(router.urls)),
    path('contact/', ContactAPIView.as_view(), name='contact'),
]
