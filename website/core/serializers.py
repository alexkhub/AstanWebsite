from abc import ABC

from rest_framework import serializers
from .models import *


class FilterImagesSerializer(serializers.ListSerializer, ABC):
    def to_representation(self, data):
        data = data.filter(first_img=True)
        return super().to_representation(data)


class ProductImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_Images
        fields = ('img', 'first_img', 'img_name')


class ProductMainImagesListSerializer(serializers.ModelSerializer):
    """вывод главной картинки """

    class Meta:
        model = Product_Images
        fields = ('img',)
        list_serializer_class = FilterImagesSerializer


class HomeProductsListSerializer(serializers.ModelSerializer):
    """сериализатор для вывода продуктов"""
    product_photos = ProductImagesListSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        read_only = ('owner.username',)
        exclude = ('numbers', 'product_characteristic', 'description', 'manufacturer', 'category')


class CategoryListSerializer(serializers.ModelSerializer):
    """сериализатор для вывода категорий"""

    class Meta:
        model = Category
        fields = ('slug', 'category_photo', 'name')


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        read_only = ('owner.username',)
        fields = ("manufacturer_name", "slug", "photo")


class ProductsListSerializer(serializers.ModelSerializer):
    """сериализатор для вывода продуктов"""
    product_photos = ProductImagesListSerializer(many=True, read_only=True)
    category = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    manufacturer = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Products
        read_only = ('owner.username',)
        exclude = ('numbers', 'product_characteristic', 'first_price', 'description',)


class ProductCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    """сериализатор для вывода продукта"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    manufacturer = serializers.SlugRelatedField(slug_field='manufacturer_name', read_only=True)
    product_photos = ProductImagesListSerializer(many=True, read_only=True)
    product_characteristic = ProductCharacteristicSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        read_only = ('owner.username',)
        exclude = ('numbers', 'date_add', 'back_to_main')


class Order_Point_ProductSerializer(serializers.ModelSerializer):
    ''''создание вложенного сериализатора'''
    product_photos = ProductImagesListSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ('id', 'product_name', 'product_photos', 'last_price', 'slug', 'numbers')
        read_only = ('owner.username',)


class Order_PointsSerializer(serializers.ModelSerializer):
    # серилизатор для вывода пунктов корзины
    user = serializers.CharField(source='user.slug')
    product = Order_Point_ProductSerializer(many=False, read_only=True)

    # если у нас 1 объект писать many= False

    class Meta:
        model = Order_Points
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    product = Order_Point_ProductSerializer(many=False, read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        read_only = ('owner.username',)
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'phone')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Comments
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        exclude = ('order_points',)