from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveProductCartSerializer, 
                         GetProductCartSerializer, 
                         UpdateProductCartSerializer, 
                         DeleteProductCartSerializer)
from django.core import serializers

from main.models import ProductCart
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class SaveProductCartView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request, format=None):
        data = {
            "user": request.user.id,
            "product":request.data.get("product_id"),
            "quantity":request.data.get("quantity"),
        }
        serializer = SaveProductCartSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Success.'},status = status.HTTP_201_CREATED)

class GetProductCartView(generics.ListAPIView):
    parser_classes = []
    def to_object(self,data):
            return {
                'user_id':data.user.id,
                'user' : data.user.name,
                'product_id':data.product.id,
                'product':data.product.name,
                'quantity':data.quantity,
                'id' : data.id
            }

    def get(self,request,format=None):
        renderer_classes = [UserRenderer]
        serializer = GetProductCartSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object,serializer.get_queryset())
        
        return Response({'data':data},status = status.HTTP_200_OK)

class UpdateProductCartView(APIView):
    queryset = ProductCart.objects.all()
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def put(self,request,pk,format = None):
        instance = ProductCart.objects.get(id=pk)
        serializer = UpdateProductCartSerializer(instance = instance, data = request.data, context = {'id':pk}, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'ProductCart updated successfully.'})

class DeleteProductCartView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated, IsAdminUser]
    def delete(self,request,pk,format = None):
        serializer = DeleteProductCartSerializer(data = request.data, context = {'id':pk})
        serializer.is_valid(raise_exception=True)
        serializer.delete_product_cart()
        return Response({'msg':'ProductCart deleted successfully.'})
         