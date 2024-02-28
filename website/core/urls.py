from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('product_category/<slug:category_slug>/', CategoryListAPIView.as_view(), name='product_category'),
    path('add_product/<int:id>/', add_product, name='add_product'),
    path('add_wishlist/<int:id>/', add_wishlist, name='add_wishlist'),
    path('show_product/<slug:slug>/', ProductRetrieveView.as_view(), name='show_product'),
]