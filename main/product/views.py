from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveProductSerializer, 
                         GetProductSerializer, 
                         UpdateProductSerializer, 
                         DeleteProductSerializer)
from django.core import serializers

from main.models import Product
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class SaveProductView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated,IsAdminUser]
    def post(self,request, format=None):
        data = {
            "name": request.data.get("name"),
            "category":request.data.get("category_id"),
            "description":request.data.get("description"),
            "image":request.FILES.get("image"),
            "price":request.data.get('price'),
            'stock':request.data.get('stock'),
        }
        serializer = SaveProductSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Success.'},status = status.HTTP_201_CREATED)

class GetProductView(generics.ListAPIView):
    parser_classes = []
    def to_object(self,data):
            print("image",data.image)
            return {
                'description':data.description,
                'name' : data.name,
                'price':data.price,
                'image':data.image.path,
                'category':data.category.name,
                'category_id':data.category.id,
                'id' : data.id,
                'stock':data.stock
            }

    def get(self,request,format=None):
        renderer_classes = [UserRenderer]
        serializer = GetProductSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object,serializer.get_queryset())
        
        return Response({'data':data},status = status.HTTP_200_OK)

class UpdateProductView(APIView):
    queryset = Product.objects.all()
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated,IsAdminUser]
    def put(self,request,pk,format = None):
        instance = Product.objects.get(id=pk)
        serializer = UpdateProductSerializer(instance = instance, data = request.data, context = {'id':pk}, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Product updated successfully.'})

class DeleteProductView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated, IsAdminUser]
    def delete(self,request,pk,format = None):
        serializer = DeleteProductSerializer(data = request.data, context = {'id':pk})
        serializer.is_valid(raise_exception=True)
        serializer.delete_product()
        return Response({'msg':'Product deleted successfully.'})
         