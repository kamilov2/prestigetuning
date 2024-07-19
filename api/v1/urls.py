from django.urls import path, include

urlpatterns = [
    path('homepage/', include('api.v1.homepage.urls')),
    path('products/', include('api.v1.products.urls')),
    path('order/', include('api.v1.order.urls')),
]
