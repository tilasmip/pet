from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from main.renderers import UserRenderer
from .serializer import (SaveCategorySerializer, 
                         GetCategorySerializer, 
                         UpdateCategorySerializer, 
                         DeleteCategorySerializer)
from django.core import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class SaveCategoryView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated, IsAdminUser]
    def post(self,request, format=None):
        serializer = SaveCategorySerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create_Category()
        return Response({'msg':'Success.'},status = status.HTTP_201_CREATED)

class GetCategoryView(APIView):
    def to_object(self,data):
            return {
                'name' : data.name,
                'id' : data.id
            }
    
    def get(self,request,format=None):
        renderer_classes = [UserRenderer]
        serializer = GetCategorySerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object,serializer.get_queryset())
        
        return Response({'data':data},status = status.HTTP_200_OK)

class UpdateCategoryView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated, IsAdminUser]
    def put(self,request,id,format = None):
        serializer = UpdateCategorySerializer(data = request.data, context = {'id':id})
        serializer.is_valid(raise_exception=True)
        serializer.update_category()
        return Response({'msg':'Category updated successfully.'})

class DeleteCategoryView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated, IsAdminUser]
    def delete(self,request,id,format = None):
        serializer = DeleteCategorySerializer(data = request.data, context = {'id':id})
        serializer.is_valid(raise_exception=True)
        serializer.delete_category()
        return Response({'msg':'Category deleted successfully.'})
         