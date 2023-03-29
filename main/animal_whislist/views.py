from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveAnimalWhislistSerializer, 
                         GetAnimalWhislistSerializer, 
                         DeleteAnimalWhislistSerializer)
from django.core import serializers

from main.models import AnimalWhislist
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class SaveAnimalWhislistView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request, format=None):
        data = {
            "user":request.user.id,
            "animal": request.data.get("animal_id"),
        }
        serializer = SaveAnimalWhislistSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Success.'},status = status.HTTP_201_CREATED)

class GetAnimalWhislistView(generics.ListAPIView):
    parser_classes = []
    def to_object(self,data):
            return {
                'animal_id':data.animal.id,
                'animal' : data.animal.breed.name,
                'animal':data.animal.description,
                'id':data.id
            }

    def get(self,request,format=None):
        renderer_classes = [UserRenderer]
        serializer = GetAnimalWhislistSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object,serializer.get_queryset())
        
        return Response({'data':data},status = status.HTTP_200_OK)


class DeleteAnimalWhislistView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def delete(self,request,pk,format = None):
        serializer = DeleteAnimalWhislistSerializer(data = request.data, context = {'id':pk, 'user':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.delete_animal_whislist()
        return Response({'msg':'AnimalWhislist deleted successfully.'})
         