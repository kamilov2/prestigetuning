from rest_framework import viewsets
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from decimal import Decimal
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, CarModelSerializer, ProductDetailSerializer
from main.models import Product, Category, Brand, CarModel

class CustomPagination(PageNumberPagination):
    allow_empty_first_page = True
    page_size = 1

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

class ProductViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    pagination_class = CustomPagination
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()  # Removed the filter for count_in_stock
        
        params = {
            'category_id': 'category__id',
            'brand_id': 'brand__id',
            'car_model_id': 'car_model__id',
            'usd_price_min': 'usd_price__gte',
            'usd_price_max': 'usd_price__lte',
            'uzs_price_min': 'uzs_price__gte',
            'uzs_price_max': 'uzs_price__lte'
        }
        
        for param, field in params.items():
            value = self.request.query_params.get(param)
            if value:
                if 'price' in field:
                    value = Decimal(value)
                queryset = queryset.filter(**{field: value})
        
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        
        serializer = self.serializer_class(page, many=True, context={'request': request}) if page is not None else self.serializer_class(queryset, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all_data(self, request):
        categories = Category.objects.all()[:6]
        brands = Brand.objects.all()[:6]
        car_models = CarModel.objects.all()[:6]
        
        category_serializer = CategorySerializer(categories, many=True)
        brand_serializer = BrandSerializer(brands, many=True)
        car_model_serializer = CarModelSerializer(car_models, many=True)
        
        return Response({
            'categories': category_serializer.data,
            'brands': brand_serializer.data,
            'car_models': car_model_serializer.data
        })

class ProductDetailViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = ProductDetailSerializer

    def list(self, request):
        product_id = request.query_params.get('id')

        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                serializer = self.serializer_class(product, context={'request': request})
                
                related_products = Product.objects.filter(category=product.category).exclude(id=product_id)[:4]
                related_products_serializer = ProductSerializer(related_products, many=True, context={'request': request})
                
                return Response({
                    'product': serializer.data,
                    'related_products': related_products_serializer.data
                })
            except Product.DoesNotExist:
                return Response({'detail': 'Product not found.'}, status=404)
        
        return Response({'detail': 'Product ID query parameter is required.'}, status=400)

class SearchProductViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def list(self, request):
        search_text = request.query_params.get('search', '')
        queryset = Product.objects.filter(
            Q(name__icontains=search_text) | 
            Q(category__name__icontains=search_text)
        ).select_related('category')
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)
