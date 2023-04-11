from django.urls import path
from main.product_cart.views import *

urlpatterns = [
    path('save', SaveProductCartView().as_view(), name='save ProductCart'),
    path('summary/save', SaveCartSummary().as_view(), name='save Summary'),
    path('get', GetProductCartView().as_view(), name='get ProductCart'),
    path('update/<pk>', UpdateProductCartView().as_view(),
         name='update ProductCart'),
    path('delete/<pk>', DeleteProductCartView().as_view(),
         name='update ProductCart'),
]
