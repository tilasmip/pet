from django.urls import path
from main.animal_whislist.views import *

urlpatterns = [
    path('save',SaveAnimalWhislistView().as_view(),name='save AnimalWhislist'),
    path('get',GetAnimalWhislistView().as_view(),name='get AnimalWhislist'),
    path('delete/<pk>',DeleteAnimalWhislistView().as_view(),name='update AnimalWhislist'),
]
