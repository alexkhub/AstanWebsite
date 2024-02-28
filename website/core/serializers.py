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


class ProductDetailSerializer(serializers.ModelSerializer):
    """сериализатор для вывода продукта"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    manufacturer = serializers.SlugRelatedField(slug_field='manufacturer_name', read_only=True)
    product_photos = ProductImagesListSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        read_only = ('owner.username',)
        exclude = ('numbers', 'product_characteristic',)
