from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeListView.as_view() , name='home'),
    path('product_category/<slug:category_slug>/', CategoryListAPIView.as_view(), name='product_category'),
]