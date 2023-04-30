from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from main.renderers import UserRenderer
from .serializer import (SaveCategorySerializer,
                         GetCategorySerializer,
                         UpdateCategorySerializer,
                         DeleteCategorySerializer)
from django.core import serializers
from main.models import Category
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class SaveCategoryView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        name = request.data.get("name")
        if name is not None:
            instance = Category(name=name)
            instance.save()
            return Response({'msg': 'Success.'}, status=status.HTTP_201_CREATED)
        return Response({'msg': 'Failed.'}, status=status.HTTP_400_BAD_REQUEST)


class GetCategoryView(APIView):
    def to_object(self, data):
        return {
            'name': data.name,
            'id': data.id
        }

    def get(self, request, format=None):
        renderer_classes = [UserRenderer]
        serializer = GetCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object, serializer.get_queryset())

        return Response({'data': data}, status=status.HTTP_200_OK)


class GetCategoryEditView(APIView):
    renderer_classes = [UserRenderer, IsAdminUser]
    queryset = Category.objects.all()

    def to_object(self, data):
        return {
            'name': data.name,
            'id': data.id
        }

    def get(self, request, id, format=None):
        if id is not None:
            instance = self.queryset.get(id=id)
            return Response({'data': self.to_object(instance)}, status=status.HTTP_200_OK)
        return Response({'msg': 'Not found.'}, status=status.HTTP_404_OK)


class UpdateCategoryView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, id, format=None):
        try:
            name = request.data.get("name")
            instance = Category.objects.get(id=id)
            instance.name = name
            instance.save()
            return Response({'msg': 'Success.'}, status=status.HTTP_200_OK)
        except:
            return Response({'msg': 'Failed.'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteCategoryView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, id, format=None):
        serializer = DeleteCategorySerializer(
            data=request.data, context={'id': id})
        serializer.is_valid(raise_exception=True)
        serializer.delete_category()
        return Response({'msg': 'Category deleted successfully.'})
