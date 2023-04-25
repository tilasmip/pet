from django.urls import path
from main.animal.views import *

urlpatterns = [
    path('save', SaveAnimalView().as_view(), name='save Animal'),
    path('top_5', GetRecentAnimalView().as_view(), name='recent Animal'),
    path('get', GetAnimalView().as_view(), name='get Animal'),
    path('admin/get', GetAdminAnimalView().as_view(), name='get Animal'),
    path('detail/<id>', DetailAnimalView().as_view(), name='get Animal'),
    path('approve/<id>', PostAproveView().as_view(), name='approve Animal'),
    path('adopt/<id>', AproveAdoption().as_view(), name='adopt Animal'),
    path('update/<pk>', UpdateAnimalView().as_view(), name='update Animal'),
    path('delete/<pk>', DeleteAnimalView().as_view(), name='update Animal'),
]
