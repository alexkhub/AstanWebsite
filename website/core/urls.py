from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('product_category/<slug:category_slug>/', CategoryListAPIView.as_view(), name='product_category'),
    path('search_product', SearchProductListView.as_view(), name='search_product'),
    path('product_brand/<slug:brand_slug>/', BrandsListAPIView.as_view(), name='product_brand'),
    path('show_product/<slug:slug>/', ProductRetrieveView.as_view(), name='show_product'),
    path('wishlist/', WishlistListView.as_view(), name='wishlist'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('account/<slug:slug>/', ProfileRetrieveView.as_view(), name='account'),
    path('shop/', ShopListView.as_view(), name='shop'),
    path('login/', LoginView.as_view(), name='login'),
    path('remove_wishlist/<int:id>/', remove_wishlist, name='remove_wishlist'),
    path('add_comment/', add_comment, name='add_comment'),
    path('cart_point_plus/<int:id>/', cart_point_plus, name='cart_point_plus'),
    path('cart_point_minus/<int:id>/', cart_point_minus, name='cart_point_minus'),
    path('cart_point_remove/<int:id>/', cart_point_remove, name='cart_point_remove'),
    path('create_order/', create_order, name='create_order'),
    path('logout/', logout_user, name='logout'),
    path('add_product/<int:id>/', add_product, name='add_product'),
    path('add_wishlist/<int:id>/', add_wishlist, name='add_wishlist'),

]