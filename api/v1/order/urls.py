from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet
    
)
app_name = 'order'

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderViewSet.as_view(), name='order'),
]