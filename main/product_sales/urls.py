from django.urls import path
from main.product_sales.views import *

urlpatterns = [
    path('save', SaveProductSalesView().as_view(), name='save ProductSales'),
    path('invoice/<refId>', GetProductSalesView().as_view(), name='get ProductSales')
]
