from django_filters import rest_framework as filters
from .models import Products




class PriceFilter(filters.FilterSet):
    last_price = filters.RangeFilter()


    class Meta:
        model = Products
        fields = ['last_price']
