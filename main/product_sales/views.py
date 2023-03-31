from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveProductSalesSerializer, 
                         GetProductSalesSerializer, 
                         UpdateProductSalesSerializer, 
                         DeleteProductSalesSerializer)
from django.core import serializers

from main.models import ProductSales
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class SaveProductSalesView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request, format=None):
        data = {
            "user": request.user.id,
            "product":request.data.get("product_id"),
            "quantity":request.data.get("quantity"),
        }
        serializer = SaveProductSalesSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Success.'},status = status.HTTP_201_CREATED)

class GetProductSalesView(generics.ListAPIView):
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
        serializer = GetProductSalesSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object,serializer.get_queryset())
        
        return Response({'data':data},status = status.HTTP_200_OK)

# class UpdateProductSalesView(APIView):
#     queryset = ProductSales.objects.all()
#     renderer_classes = [UserRenderer]
#     permission_classes=[IsAuthenticated]
#     def put(self,request,pk,format = None):
#         instance = ProductSales.objects.get(id=pk)
#         serializer = UpdateProductSalesSerializer(instance = instance, data = request.data, context = {'id':pk}, partial = True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'msg':'ProductSales updated successfully.'})

# class DeleteProductSalesView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes=[IsAuthenticated, IsAdminUser]
#     def delete(self,request,pk,format = None):
#         serializer = DeleteProductSalesSerializer(data = request.data, context = {'id':pk})
#         serializer.is_valid(raise_exception=True)
#         serializer.delete_product_sales()
#         return Response({'msg':'ProductSales deleted successfully.'})
         