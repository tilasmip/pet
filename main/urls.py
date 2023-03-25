
from django.urls import path
from main.views import *

urlpatterns = [
    path('user/register',UserRegistrationView.as_view(), name='register'),
    path('user/login',UserLoginView.as_view(),name='login'),
    path('user/profile',UserProfileView.as_view(), name='profle'),
    path('user/change-password',UserChangePasswordView.as_view(),name='change password'),
    path('user/request-password-reset',UserRequestPasswordResetView.as_view(),name='request reset password'),
    path('user/reset-pasword/<uid>/<token>',UserPasswordResetView.as_view(),name='reset password'),
]
