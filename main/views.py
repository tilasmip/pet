from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from django.core import serializers
from main.enums import Gender

from main.models import Animal, Product, Adoption, User, CartSummary
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class GetDashboardOverview(generics.ListAPIView):
    parser_classes = []
    renderer_classes = [UserRenderer,]

    def get(self, request, format=None):
        if self.request.user.is_authenticated and self.request.user.is_admin:
            data = {
                'animals': Animal.objects.count(),
                'products': Product.objects.count(),
                'adoptions': Adoption.objects.count(),
                'users': User.objects.count()
            }
            return Response({'data': data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
