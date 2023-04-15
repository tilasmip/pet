from django.urls import path
from main.product_wishlist.views import *

urlpatterns = [
    path('save', SaveProductWishlistView().as_view(),
         name='save ProductWishlist'),
    path('get', GetProductWishlistView().as_view(), name='get ProductWishlist'),
    path('delete/<pk>', DeleteProductWishlistView().as_view(),
         name='update ProductWishlist'),
]
