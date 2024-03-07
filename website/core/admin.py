from django.contrib import admin
from django.db.models import Prefetch
from django.utils.safestring import mark_safe

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_login', 'username', 'email', 'phone', 'is_staff', )
    list_display_links = ('id', 'last_login', 'username', 'email', 'phone',)
    search_fields = ('id', 'username', 'phone', 'email')
    list_filter = ('is_staff',)
    list_editable = ('is_staff',)


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'manufacturer_name', 'country', 'get_image')
    list_display_links = ('manufacturer_name',)
    search_fields = ('manufacturer_name', 'country')
    list_filter = ('country',)
    prepopulated_fields = {"slug": ("manufacturer_name",)}

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="60" height="60"')

    get_image.short_description = "Логотип"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_image')
    readonly_fields = ('get_image',)
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.category_photo.url} width="60" height="60"')

    get_image.short_description = "Изображение категории"


class Product_ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_name', 'first_img', 'get_image')
    readonly_fields = ('get_image',)
    list_display_links = ('img_name',)
    prepopulated_fields = {'slug': ('img_name',)}
    search_fields = ('img_name',)
    list_editable = ('first_img',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.img.url} width="60" height="60"')

    get_image.short_description = "Изображение продукта"


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product_name', 'first_price', 'last_price', 'discount', 'category', 'manufacturer')
    list_display_links = ('id', 'product_name')
    search_fields = ('product_name',)
    list_filter = ('discount', 'category', 'manufacturer', 'last_price',)
    list_editable = ('first_price', 'last_price', 'discount')
    prepopulated_fields = {'slug': ('product_name',)}

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related(
            'category',
            'manufacturer',
            'product_photos')
        return queryset


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'text', 'rating', 'date')
    list_filter = ('rating', 'product')
    search_fields = ('user', 'product')


class EmailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_display_links = ('id', 'email')


class CharacteristicAdmin(admin.ModelAdmin):
    list_display = ('id', 'characteristic_name', 'value')
    list_display_links = ('id', 'characteristic_name')


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'date')
    prepopulated_fields = {'slug': ('user', 'product')}


class Order_PointsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'amount', 'price', 'in_orders')
    list_display_links = ('product', 'user')
    list_filter = ('product', 'user')
    search_fields = ('product', 'user')
    list_editable = ('in_orders',)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_order_points', 'payment_status', 'fulfillment_status', 'price',)
    list_display_links = ('id', 'user',)
    search_fields = ('id', 'user')
    list_filter = ('price', 'date', 'payment_status', 'fulfillment_status')
    list_editable = ('payment_status', 'fulfillment_status')

    @admin.display(description='пункты заказа')
    def get_order_points(self, obj):
        return [order_point.pk for order_point in obj.order_points.all()]


admin.site.register(Order_Points, Order_PointsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(Users, UserAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product_Images, Product_ImagesAdmin)
admin.site.register(Products, ProductAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(Wishlist, WishlistAdmin)
