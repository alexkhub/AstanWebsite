from django.db.models import Q, Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .models import *
from .serializers import *

class HomeListView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/index.html'

    def list(self, request, **kwargs):
        products = Products.objects.filter(Q(discount=0) & Q(numbers__gt=0)).prefetch_related(
            Prefetch('product_photos', queryset=Product_Images.objects.filter(first_img=True))).only(
            'id', 'numbers', 'product_photos', 'discount', 'product_name', 'last_price', 'slug')  # товары без скидки

        products_with_discount = Products.objects.filter(Q(discount__gt=0) & Q(numbers__gt=0)).prefetch_related(
            Prefetch('product_photos', queryset=Product_Images.objects.filter(first_img=True))).only(
            "id", 'numbers', 'product_photos', 'discount', 'product_name', 'last_price', 'slug')  # товары со скидкой

        categories =  categories = Category.objects.all().only('slug', 'category_photo', 'name')
        manufacturer = Manufacturer.objects.all().only('slug', 'photo', 'manufacturer_name')
        manufacturer_serializer = ManufacturerSerializer(manufacturer, many=True)
        products_serializer = HomeProductsListSerializer(products, many=True)
        products_with_discount_serializer = HomeProductsListSerializer(products_with_discount, many=True)
        category_serializer = CategoryListSerializer(categories, many=True)

        return Response(
            {'products_serializer': products_serializer.data,
             'products_with_discount_serializer': products_with_discount_serializer.data,
             'category_serializer': category_serializer.data,
             'manufacturer_serializer': manufacturer_serializer.data
             }
        )