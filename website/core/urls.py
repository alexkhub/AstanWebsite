from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('product_category/<slug:category_slug>/', CategoryListAPIView.as_view(), name='product_category'),
    path('add_product/<int:id>/', add_product, name='add_product'),
    path('add_wishlist/<int:id>/', add_wishlist, name='add_wishlist'),
    path('show_product/<slug:slug>/', ProductRetrieveView.as_view(), name='show_product'),
    path('wishlist/', WishlistListView.as_view(), name='wishlist'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('account/<slug:slug>/', ProfileRetrieveView.as_view(), name='account'),
    path('login/', LoginView.as_view(), name='login'),
    path('remove_wishlist/<int:id>/', remove_wishlist, name='remove_wishlist'),
    path('add_comment/', add_comment, name='add_comment'),
]