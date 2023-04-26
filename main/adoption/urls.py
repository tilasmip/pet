from django.urls import path
from main.adoption.views import *

urlpatterns = [
    path('save', SaveAdoptionView().as_view(), name='save Adoption'),
    path('get', GetAdoptionView().as_view(), name='save Adoption'),
    path('reject/<pk>', RejectdoptionView().as_view(), name='reject Adoption'),
    path('accept/<pk>', AcceptdoptionView().as_view(), name='accept Adoption'),
    path('delete/<pk>', DeleteAdoptionView().as_view(), name='Delete Adoption'),
    path('update/<pk>', UpdateAdoptionView().as_view(), name='update Adoption'),
]
