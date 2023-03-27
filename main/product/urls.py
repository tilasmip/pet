from django.urls import path
from main.product.views import *

urlpatterns = [
    path('save',SaveProductView().as_view(),name='save Product'),
    path('get',GetProductView().as_view(),name='get Product'),
    path('update/<pk>',UpdateProductView().as_view(),name='update Product'),
    path('delete/<pk>',DeleteProductView().as_view(),name='update Product'),
]
