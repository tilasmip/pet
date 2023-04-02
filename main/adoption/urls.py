from django.urls import path
from main.adoption.views import *

urlpatterns = [
    path('save', SaveAdoptionView().as_view(), name='save Adoption'),
    path('delete/<pk>', DeleteAdoptionView().as_view(), name='Delete Adoption'),
    path('update/<pk>', UpdateAdoptionView().as_view(), name='update Adoption'),
]
