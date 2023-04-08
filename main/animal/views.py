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
            "name": request.data.get("name"),
            "age": request.data.get("age"),
            "gender": request.data.get("gender"),
            "likes": request.data.get("likes"),
            "personality": request.data.get("personality"),
            "category": request.data.get("category"),
            "breed": request.data.get("breed"),
            "image": request.FILES.get("image"),
            "posted_by": request.user.id

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


class GetRecentAnimalView(generics.ListAPIView):
    parser_classes = []

    def to_object(self, data):
        return {
            'description': data.description,
            'breed': data.breed.name,
            "popularity": data.popularity,
            "personality": data.personality,
            "likes": data.likes,
            "name": data.name,
            "age": data.age,
            "gender": data.gender,
            'breed': data.breed.name,
            'image': data.image.path,
            'category': data.category.name,
            'id': data.id
        }
    queryset = Animal.objects.all()

    def get(self, request, format=None):
        renderer_classes = [UserRenderer]
        animals = self.queryset.order_by("-created_at")[:5]
        data = map(self.to_object, animals)

        return Response({'data': data}, status=status.HTTP_200_OK)


class GetAnimalView(generics.ListAPIView):
    parser_classes = []

    def to_object(self, data):
        return {
            'description': data.description,
            'breed': data.breed.name,
            "popularity": data.popularity,
            "personality": data.personality,
            "likes": data.likes,
            "name": data.name,
            "age": data.age,
            "gender": data.gender,
            'breed': data.breed.id,
            'image': data.image.path,
            'category': data.category.name,
            'category': data.category.id,
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
