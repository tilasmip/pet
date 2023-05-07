
from django.urls import path
from main.user.views import *

urlpatterns = [
    path('get', UserGetView.as_view(), name='getu ser'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserProfileView.as_view(), name='profle'),
    path('update', ProfileUpdateView.as_view(), name='update'),
    path('is_authenticated', UserIsAuthenticatedView.as_view(),
         name='isAuthenticated'),
    path('change-password', UserChangePasswordView.as_view(), name='change password'),
    path('request-password-reset', UserRequestPasswordResetView.as_view(),
         name='request reset password'),
    path('reset-pasword/<uid>/<token>',
         UserPasswordResetView.as_view(), name='reset password'),
]
