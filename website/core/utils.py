from django_filters import rest_framework as filters
from .models import Products, Category, Manufacturer
class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass
class ProductFilter(filters.FilterSet):
    last_price = filters.RangeFilter()
    category = CharFilterInFilter(field_name='category__slug', lookup_expr='in')
    manufacturer = CharFilterInFilter(field_name='manufacturer__slug', lookup_expr='in')
    discount = filters.BooleanFilter(field_name='discount', lookup_expr='gte')

    class Meta:
        model = Products
        fields = ['last_price', 'category', 'manufacturer', 'discount']
