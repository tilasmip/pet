from django.urls import path
from main.product.views import *

urlpatterns = [
    path('get', GetProductView().as_view(), name='get Product'),
    path('top_5', RecentProductView.as_view(), name='top five'),
    # path('save',SaveProductView().as_view(),name='save Product'),
    # path('update/<pk>',UpdateProductView().as_view(),name='update Product'),
    # path('delete/<pk>',DeleteProductView().as_view(),name='update Product'),
]
