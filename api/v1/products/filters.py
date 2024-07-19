from django_filters import rest_framework as filters
from main.models import Product

class ProductFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category__id', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['category']
