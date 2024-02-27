from django.db.models import Q, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .utils import *
from .models import *
from .serializers import *

class HomeListView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/index.html'

    def list(self, request, **kwargs):
        products = Products.objects.filter( numbers__gt=0).prefetch_related(
            Prefetch('product_photos', queryset=Product_Images.objects.filter(first_img=True))).only(
            'id', 'numbers', 'product_photos', 'discount', 'product_name', 'last_price', 'slug')


        categories = Category.objects.all().only('slug', 'category_photo', 'name')
        manufacturer = Manufacturer.objects.all().only('slug', 'photo', 'manufacturer_name')
        manufacturer_serializer = ManufacturerSerializer(manufacturer, many=True)
        products_serializer = HomeProductsListSerializer(products, many=True)

        category_serializer = CategoryListSerializer(categories, many=True)

        return Response(
            {'products_serializer': products_serializer.data,

             'category_serializer': category_serializer.data,
             'manufacturer_serializer': manufacturer_serializer.data
             }
        )

class CategoryListAPIView(ListAPIView):
    queryset = Products.objects.filter(numbers__gt=0).prefetch_related(
        Prefetch('product_photos', queryset=Product_Images.objects.filter(first_img=True)),
        Prefetch('manufacturer', queryset=Manufacturer.objects.all().only('slug')),
        Prefetch('category', queryset=Category.objects.all().only('slug', 'name'))
    ).only(
        'id', 'numbers', 'manufacturer', 'product_photos', 'category', 'discount',
        'product_name', 'last_price', 'slug')
    #
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'shop/catalog.html'

    serializer_class = ProductsListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self):
        self.queryset = self.queryset.filter(category__slug=self.request.resolver_match.kwargs['category_slug'])
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        categories = Category.objects.all().only('slug', 'category_photo', 'name')
        manufacturer = Manufacturer.objects.all().only('slug', 'photo', 'manufacturer_name')
        manufacturer_serializer = ManufacturerSerializer(manufacturer, many=True)
        category_serializer = CategoryListSerializer(categories, many=True)
        serializer_products = self.get_serializer(queryset, many=True)
        return Response({'products': serializer_products.data,
                         'categories': category_serializer.data,
                         'manufacturers': manufacturer_serializer.data
                         })