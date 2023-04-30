from django.urls import path
from main.breed.views import *

urlpatterns = [
    path('save', SaveBreedView().as_view(), name='save Breed'),
    path('get', GetBreedView().as_view(), name='get Breed'),
    path('get/<id>', GetBreedEditView().as_view(), name='get Breed for edit'),
    path('update/<id>', UpdateBreedView().as_view(), name='update Breed'),
    path('delete/<id>', DeleteBreedView().as_view(), name='update Breed'),
]
