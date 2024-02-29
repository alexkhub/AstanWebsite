from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import *
from .models import *
from .serializers import *


class HomeListView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/index.html'

    def list(self, request, **kwargs):
        products = Products.objects.filter(Q(numbers__gt=0) & Q(back_to_main=True)).prefetch_related(
            Prefetch('product_photos', queryset=Product_Images.objects.filter(first_img=True))).only(
            'id', 'numbers', 'product_photos', 'first_price', 'discount', 'product_name', 'last_price', 'slug',
            'back_to_main', 'date_add')[:12]

        new_products = Products.objects.filter(numbers__gt=0, ).prefetch_related(
            Prefetch('product_photos', queryset=Product_Images.objects.filter(first_img=True))).only(
            'id', 'numbers', 'product_photos', 'first_price', 'discount', 'product_name', 'last_price', 'slug',
            'back_to_main', 'date_add').order_by('date_add')[:7]
        categories = Category.objects.all().only('slug', 'category_photo', 'name')

        manufacturer = Manufacturer.objects.all().only('slug', 'photo', 'manufacturer_name')
        manufacturer_serializer = ManufacturerSerializer(manufacturer, many=True)
        products_serializer = HomeProductsListSerializer(products, many=True)
        new_products_serializer = HomeProductsListSerializer(new_products, many=True)
        category_serializer = CategoryListSerializer(categories, many=True)

        return Response(
            {'products_serializer': products_serializer.data,
             'new_products_serializer': new_products_serializer.data,
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


class ProductRetrieveView(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/product-details.html'
    lookup_field = "slug"
    queryset = Products.objects.prefetch_related(
        Prefetch('manufacturer', queryset=Manufacturer.objects.all().only('manufacturer_name')),
        Prefetch('category', queryset=Category.objects.all().only('name')),

    ).only(
        'id', 'numbers', 'manufacturer', 'product_photos', 'category', 'discount',
        'product_name', 'last_price', 'description', 'first_price', 'slug')
    serializer_class = ProductDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        product_serializer = self.get_serializer(self.get_object())
        return Response({'product': product_serializer.data})


@login_required(login_url='login')
def add_product(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Products.objects.get(id=id)
    user = request.user
    if not Order_Points.objects.filter(user=user, product=product, in_orders=False):
        Order_Points.objects.create(
            user=user,
            product=product
        )
        return redirect(url)
    else:
        return redirect('home')


class CartListView(ListAPIView):
    queryset = Order_Points.objects.filter(in_orders=False)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/cart.html'
    serializer_class = Order_PointsSerializer
    permission_classes = [IsAuthenticated]

    # lookup_field = 'slug'

    def get_queryset(self):
        self.queryset = self.queryset.filter(user=self.request.user).prefetch_related(
            Prefetch('product', queryset=Products.objects.all().prefetch_related(
                Prefetch('product_photos', queryset=Product_Images.objects.filter(first_img=True)
                         .only('img', 'first_img', 'img_name')))
                     .only('id', 'numbers', 'product_photos', 'discount', 'product_name', 'description',
                           'last_price', )
                     ),
            Prefetch('user', queryset=Users.objects.all().only('slug')),
        )
        return self.queryset

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'order_points': serializer.data
            }
            # serializer.data
        )


class WishlistListView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/wishlist.html'
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'wishlist': serializer.data
            }
            # serializer.data
        )

class ProfileRetrieveView(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/my-account.html'
    queryset = Users.objects.all().only('id', 'first_name', 'password', 'last_name',
                                        'username', 'date_joined', 'phone', 'slug', )
    serializer_class = UserSerializer
    lookup_field = "slug"
    permission_classes = (IsAuthenticated,)


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/login.html'


@login_required(login_url='auth/login/')
def add_wishlist(request, id):
    url = request.META.get('HTTP_REFERER')
    product = Products.objects.get(id=id)
    user = request.user
    if not Wishlist.objects.filter(Q(user=user) & Q(product=product)).first():
        Wishlist.objects.create(
            user=user,
            product=product
        )
        return redirect(url)
    else:
        return redirect('home')
