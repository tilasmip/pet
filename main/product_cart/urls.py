from django.urls import path
from main.product_cart.views import *

urlpatterns = [
    path('save', SaveProductCartView().as_view(), name='save ProductCart'),
    path('payment/proceed/<pk>', ProceedPaymentView().as_view(),
         name='proceed payment'),
    path('payment/complete/<pk>',
         CompletePaymentView().as_view(), name='complte payment'),
    path('get', GetProductCartView().as_view(), name='get ProductCart'),
    path('invoice/<id>', PurchaseInvoiceView().as_view(),
         name='get invoice'),
    path('delete/<pk>', DeleteProductCartView().as_view(),
         name='update ProductCart'),
]
