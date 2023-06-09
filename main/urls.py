
from django.urls import path, include
from main.user.views import *
from main.views import *

urlpatterns = [
    path('user/', include('main.user.urls')),
    path('admin/dashboard/', GetDashboardOverview.as_view(),
         name="get dashboard detail"),
    path('product/', include('main.product.urls')),
    path('category/', include('main.category.urls')),
    path('breed/', include('main.breed.urls')),
    path('animal/', include('main.animal.urls')),
    path('animal_wishlist/', include('main.animal_wishlist.urls')),
    path('product_wishlist/', include('main.product_wishlist.urls')),
    path('product_cart/', include('main.product_cart.urls')),
    path('adoption/', include('main.adoption.urls')),
]
