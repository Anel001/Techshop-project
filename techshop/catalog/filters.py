from django_filters import FilterSet
import django_filters
from .models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
        }



class ProductFilterset(FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    rating__gt = django_filters.NumberFilter(field_name='rating', lookup_expr='gt')
    rating__lt = django_filters.NumberFilter(field_name='rating', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['inStock', 'producer', 'price', 'rating']

