from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from main.renderers import UserRenderer
from .serializer import (SaveBreedSerializer, 
                         GetBreedSerializer, 
                         UpdateBreedSerializer, 
                         DeleteBreedSerializer)
from django.core import serializers

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class SaveBreedView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated, IsAdminUser]
    def post(self,request, format=None):
        serializer = SaveBreedSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create_Breed()
        return Response({'msg':'Success.'},status = status.HTTP_201_CREATED)

class GetBreedView(APIView):
    def to_object(self,data):
            return {
                'name' : data.name,
                'category':data.category.name,
                'category_id':data.category.id,
                'id' : data.id
            }
    
    def get(self,request,format=None):
        renderer_classes = [UserRenderer]
        serializer = GetBreedSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object,serializer.get_queryset())
        
        return Response({'data':data},status = status.HTTP_200_OK)

class UpdateBreedView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated, IsAdminUser]
    def put(self,request,id,format = None):
        serializer = UpdateBreedSerializer(data = request.data, context = {'id':id})
        serializer.is_valid(raise_exception=True)
        serializer.update_breed()
        return Response({'msg':'Breed updated successfully.'})

class DeleteBreedView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated, IsAdminUser]
    def delete(self,request,id,format = None):
        serializer = DeleteBreedSerializer(data = request.data, context = {'id':id})
        serializer.is_valid(raise_exception=True)
        serializer.delete_category()
        return Response({'msg':'Breed deleted successfully.'})
         