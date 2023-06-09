from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveAnimalWishlistSerializer,
                         GetAnimalWishlistSerializer,
                         DeleteAnimalWishlistSerializer)
from django.core import serializers

from main.models import AnimalWishlist
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class SaveAnimalWishlistView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = {
            "user": request.user.id,
            "animal": request.data.get("animal_id"),
        }
        serializer = SaveAnimalWishlistSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Success.'}, status=status.HTTP_201_CREATED)


class GetAnimalWishlistView(generics.ListAPIView):
    parser_classes = []
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def toobject(self, data):
        if (data.animal.image.name is not None):
            name = data.animal.image.name.split("/")[-1]
        else:
            name = "default_animal.png"
        return {
            'breed': data.animal.breed.name,
            'name': data.animal.name,
            'addedDate': str(data.created_at),
            'postedBy': self.request.user.email.split("@")[0],
            'description': data.animal.description,
            'image': name,
            'id': data.id
        }

    def get(self, request, format=None):
        serializer = GetAnimalWishlistSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        result = serializer.get_queryset()
        data = []
        for item in result:
            data.append(self.toobject(item))

        return Response({'data': data}, status=status.HTTP_200_OK)


class DeleteAnimalWishlistView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        serializer = DeleteAnimalWishlistSerializer(
            data=request.data, context={'id': pk, 'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.delete_animal_wishlist()
        return Response({'msg': 'AnimalWishlist deleted successfully.'})
