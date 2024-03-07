from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch, Sum
from django.shortcuts import redirect, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CreateComment
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
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/shop.html'

    serializer_class = ProductsListSerializer
    filter_backends = (DjangoFilterBackend,)


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


class BrandsListAPIView(ListAPIView):
    queryset = Products.objects.filter(numbers__gt=0).prefetch_related(
        Prefetch('product_photos', queryset=Product_Images.objects.filter(first_img=True)),
        Prefetch('manufacturer', queryset=Manufacturer.objects.all().only('slug')),
        Prefetch('category', queryset=Category.objects.all().only('slug', 'name'))
    ).only(
        'id', 'numbers', 'manufacturer', 'product_photos', 'category', 'discount',
        'product_name', 'last_price', 'slug')
    #
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/shop.html'

    serializer_class = ProductsListSerializer
    filter_backends = (DjangoFilterBackend,)


    def get_queryset(self):
        self.queryset = self.queryset.filter(category__slug=self.request.resolver_match.kwargs['brand_slug'])
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
    queryset = Products.objects.all().select_related('manufacturer', 'category').only(
        'id', 'numbers', 'manufacturer', 'product_photos', 'category', 'discount',
        'product_name', 'last_price', 'description', 'first_price', 'slug')
    serializer_class = ProductDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        product_serializer = self.get_serializer(obj)
        comment = Comments.objects.filter(product=obj).select_related('user')
        comment_serializer = CommentSerializer(comment, many=True)
        return Response({
            'product': product_serializer.data,
            'comments': comment_serializer.data,
            'x': [1, 2, 3, 4, 5]
        })


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
                           'last_price', "slug")
                     ),
            Prefetch('user', queryset=Users.objects.all().only('slug')),
        )
        return self.queryset

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        manufacturer = Manufacturer.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        manufacturer_serializer = ManufacturerSerializer(manufacturer, many=True)
        return Response(
            {
                'order_points': serializer.data,
                'manufacturers': manufacturer_serializer.data
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
        )


class ProfileRetrieveView(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/my-account.html'
    queryset = Users.objects.all().only('id', 'first_name', 'password', 'last_name',
                                        'username', 'date_joined', 'phone', 'slug', )
    serializer_class = UserSerializer
    lookup_field = "slug"
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        orders = Orders.objects.filter(user=instance)
        orders_serializer = OrdersSerializer(orders, many=True)
        serializer = self.get_serializer(instance)
        return Response({
            'user': serializer.data,
            'orders': orders_serializer.data
        }
        )


class LoginView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/login.html'

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return redirect('home')
        return redirect('login')

    def get(self, request, format=None):
        return Response()


class ShopListView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/shop.html'

    queryset = Products.objects.filter(numbers__gt=0).prefetch_related(
        Prefetch('product_photos', queryset=Product_Images.objects.filter(first_img=True)),
        Prefetch('manufacturer', queryset=Manufacturer.objects.all().only('slug')),
        Prefetch('category', queryset=Category.objects.all().only('slug', 'name'))
    ).only(
        'id', 'numbers', 'manufacturer', 'product_photos', 'category', 'discount',
        'product_name', 'last_price', 'slug')

    serializer_class = ProductsListSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        categories = Category.objects.all().only('slug', 'category_photo', 'name')
        manufacturer = Manufacturer.objects.all().only('slug', 'photo', 'manufacturer_name')
        serializer_products = self.get_serializer(queryset, many=True)
        manufacturer_serializer = ManufacturerSerializer(manufacturer, many=True)
        category_serializer = CategoryListSerializer(categories, many=True)

        return Response({'products': serializer_products.data,
                         'categories': category_serializer.data,
                         'manufacturers': manufacturer_serializer.data
                         }
                        )






@login_required(login_url='login')
def add_product(request, id):
    product = Products.objects.get(id=id)
    if not Order_Points.objects.filter(user=request.user, product=product, in_orders=False):
        Order_Points.objects.create(
            user=request.user,
            product=product
        )
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('home')


@login_required(login_url='login')
def add_wishlist(request, id):
    product = Products.objects.get(id=id)
    if not Wishlist.objects.filter(Q(user=request.user) & Q(product=product)).first():
        Wishlist.objects.create(
            user=request.user,
            product=product
        )
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('home')


@login_required(login_url='login')
def remove_wishlist(request, id):
    wishlist = Wishlist.objects.get(id=id)
    if wishlist.user == request.user:
        wishlist.delete()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect("home")


@login_required(login_url='login')
def add_comment(request):
    if request.POST:
        form = CreateComment(request.POST)
        url = request.META.get('HTTP_REFERER')
        product_slug = url.split('/')[-2]
        if form.is_valid():
            product = Products.objects.get(slug=product_slug)
            Comments.objects.create(
                user=request.user,
                rating=form.data['rating'],
                product=product,
                text=form.data['text']
            )
        return redirect(url)


def cart_point_plus(request, id):
    cart_point = get_object_or_404(Order_Points, id=id)
    cart_point.amount += 1
    cart_point.save()
    return redirect(request.META['HTTP_REFERER'])


def cart_point_minus(request, id):
    cart_point = get_object_or_404(Order_Points, id=id)
    if cart_point.amount > 1:
        cart_point.amount -= 1
        cart_point.save()

    else:
        cart_point.delete()
    return redirect(request.META['HTTP_REFERER'])


def cart_point_remove(request, id):
    cart_point = get_object_or_404(Order_Points, id=id)
    cart_point.delete()
    return redirect(request.META['HTTP_REFERER'])


def create_order(request):
    try:
        cart_points = Order_Points.objects.filter(Q(in_orders=False) & Q(user=request.user))

        order = Orders.objects.create(
            user=request.user,
            price=cart_points.aggregate(Sum("price"))['price__sum']
        )
        for cart_point in cart_points:
            order.order_points.add(cart_point)
        order.save()

        cart_points.update(in_orders=True)
    except BaseException:
        pass

    return redirect("home")


def logout_user(request):
    logout(request)
    return redirect('home')
