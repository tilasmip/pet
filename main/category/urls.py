from django.urls import path
from main.category.views import *

urlpatterns = [
    path('save',SaveCategoryView().as_view(),name='save category'),
    path('get',GetCategoryView().as_view(),name='get category'),
    path('update/<id>',UpdateCategoryView().as_view(),name='update category'),
    path('delete/<id>',DeleteCategoryView().as_view(),name='update category'),
]
