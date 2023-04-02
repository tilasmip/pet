from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveAnimalSerializer,
                         GetAnimalSerializer,
                         UpdateAnimalSerializer,
                         DeleteAnimalSerializer)
from django.core import serializers

from main.models import Animal
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class SaveAnimalView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = {
            "popularity": request.data.get("popularity", 0),
            "category": request.data.get("category_id"),
            "breed": request.data.get("breed_id"),
            "image": request.FILES.get("image"),
            "posted_by": request.data.get("posted_by_id")

        }
        serializer = SaveAnimalSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Success.'}, status=status.HTTP_201_CREATED)


class UpdatePopularityView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        instance = Animal.objects.get(id=pk)
        serializer = UpdateAnimalSerializer(
            instance=instance, data=request.data, context={'id': pk}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Animal updated successfully.'})


class GetAnimalView(generics.ListAPIView):
    parser_classes = []

    def to_object(self, data):
        return {
            'description': data.description,
            'breed': data.breed.name,
            'breed_id': data.breed.id,
            'image': data.image.path,
            'category': data.category.name,
            'category_id': data.category.id,
            'id': data.id
        }

    def get(self, request, format=None):
        renderer_classes = [UserRenderer]
        serializer = GetAnimalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object, serializer.get_queryset())

        return Response({'data': data}, status=status.HTTP_200_OK)


class UpdateAnimalView(APIView):
    queryset = Animal.objects.all()
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        instance = Animal.objects.get(id=pk)
        serializer = UpdateAnimalSerializer(
            instance=instance, data=request.data, context={'id': pk}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Animal updated successfully.'})


class DeleteAnimalView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk, format=None):
        serializer = DeleteAnimalSerializer(
            data=request.data, context={'id': pk})
        serializer.is_valid(raise_exception=True)
        serializer.delete_animal()
        return Response({'msg': 'Animal deleted successfully.'})
