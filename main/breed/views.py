from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from main.renderers import UserRenderer
from .serializer import (SaveBreedSerializer,
                         GetBreedSerializer,
                         UpdateBreedSerializer,
                         DeleteBreedSerializer)
from django.core import serializers
from main.models import Breed, Category
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class SaveBreedView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        name = request.data.get("name")
        category = Category.objects.get(id=request.data.get("category"))
        instance = Breed(name=name, category=category)
        instance.save()
        return Response({'msg': 'Success.'}, status=status.HTTP_201_CREATED)


class GetBreedView(APIView):
    def to_object(self, data):
        return {
            'name': data.name,
            'category': data.category.name,
            'category_id': data.category.id,
            'id': data.id
        }

    def get(self, request, format=None):
        renderer_classes = [UserRenderer]
        serializer = GetBreedSerializer(data=request.data, context={
                                        'category': request.GET.get('category')})
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object, serializer.get_queryset())

        return Response({'data': data}, status=status.HTTP_200_OK)


class GetBreedEditView(APIView):
    renderer_classes = [UserRenderer, IsAdminUser]
    queryset = Breed.objects.all()

    def to_object(self, data):
        return {
            'name': data.name,
            'category': data.category.name,
            'category_id': data.category.id,
            'id': data.id
        }

    def get(self, request, id, format=None):
        if id is not None:
            instance = self.queryset.get(id=id)
            return Response({'data': self.to_object(instance)}, status=status.HTTP_200_OK)
        return Response({'msg': 'Not found.'}, status=status.HTTP_404_OK)


class UpdateBreedView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, id, format=None):
        try:
            name = request.data.get("name")
            category = Category.objects.get(id=request.data.get("category"))
            instance = Breed.objects.get(id=id)
            instance.name = name
            instance.category = category
            instance.save()
            return Response({'msg': 'Success.'}, status=status.HTTP_200_OK)
        except:
            return Response({'msg': 'Failed.'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteBreedView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, id, format=None):
        serializer = DeleteBreedSerializer(
            data=request.data, context={'id': id})
        serializer.is_valid(raise_exception=True)
        serializer.delete_breed()
        return Response({'msg': 'Breed deleted successfully.'})
