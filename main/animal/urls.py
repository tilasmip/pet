from django.urls import path
from main.animal.views import *

urlpatterns = [
    path('save', SaveAnimalView().as_view(), name='save Animal'),
    path('top_5', GetRecentAnimalView().as_view(), name='recent Animal'),
    path('get', GetAnimalView().as_view(), name='get Animal'),
    path('update/<pk>', UpdateAnimalView().as_view(), name='update Animal'),
    path('delete/<pk>', DeleteAnimalView().as_view(), name='update Animal'),
]
