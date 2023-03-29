from django.urls import path
from main.product_whislist.views import *

urlpatterns = [
    path('save',SaveProductWhislistView().as_view(),name='save ProductWhislist'),
    path('get',GetProductWhislistView().as_view(),name='get ProductWhislist'),
    path('delete/<pk>',DeleteProductWhislistView().as_view(),name='update ProductWhislist'),
]
