from django.urls import path
from main.animal_wishlist.views import *

urlpatterns = [
    path('save', SaveAnimalWishlistView().as_view(), name='save AnimalWishlist'),
    path('get', GetAnimalWishlistView().as_view(), name='get AnimalWishlist'),
    path('delete/<pk>', DeleteAnimalWishlistView().as_view(),
         name='update AnimalWishlist'),
]
