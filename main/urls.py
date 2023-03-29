
from django.urls import path, include
from main.user.views import *
from main.product import views 

urlpatterns = [
    path('user/',include('main.user.urls')),
    path('product/',include('main.product.urls')),
    path('category/',include('main.category.urls')),
    path('breed/',include('main.breed.urls')),
    path('animal/',include('main.animal.urls')),
    path('animal_whislist/',include('main.animal_whislist.urls')),
    path('product_whislist/',include('main.product_whislist.urls')),
]
