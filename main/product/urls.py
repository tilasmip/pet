
from django.urls import path
from main.product.views import *

urlpatterns = [
    path('save',SaveProductView().as_view(),name='save product'),
]
