from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveProductCartSerializer,
                         GetProductCartSerializer,
                         UpdateProductCartSerializer,
                         DeleteProductCartSerializer,
                         SaveCartSummarySerializer)
from django.core import serializers

from main.models import ProductCart
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class SaveProductCartView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = {
            "user": request.user.id,
            "product": request.data.get("product_id"),
            "quantity": request.data.get("quantity", 1),
        }
        serializer = SaveProductCartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Success.'}, status=status.HTTP_201_CREATED)


class SaveCartSummary(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = {
            "user": request.user.id,
            "amount": request.data.get("amount"),
            "shipping_address": request.data.get("shipping_address"),
            "additional_info": request.data.get("additional_info"),
        }
        serializer = SaveCartSummarySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({'msg': instance.id}, status=status.HTTP_201_CREATED)


class GetProductCartView(generics.ListAPIView):
    parser_classes = []

    def to_object(self, data):
        if (data.product.image is not None):
            name = data.product.image.name.split("/")[-1]
        else:
            name = ""
        print(data.product.image)
        return {
            'user_id': data.user.id,
            'user': data.user.name,
            'image': name,
            'category': data.product.category.name,
            'product': data.product.name,
            'price': data.product.price,
            'stock': data.product.stock,
            'quantity': data.quantity,
            'id': data.id
        }

    def get(self, request, format=None):
        renderer_classes = [UserRenderer]
        permission_classes = [IsAuthenticated]
        serializer = GetProductCartSerializer(
            data=request.data, context={'user': request.user.id})
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object, serializer.get_queryset())

        return Response({'data': data}, status=status.HTTP_200_OK)


class UpdateProductCartView(APIView):
    queryset = ProductCart.objects.all()
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        instance = ProductCart.objects.get(id=pk)
        serializer = UpdateProductCartSerializer(
            instance=instance, data=request.data, context={'id': pk}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'ProductCart updated successfully.'})


class DeleteProductCartView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk, format=None):
        serializer = DeleteProductCartSerializer(
            data=request.data, context={'id': pk})
        serializer.is_valid(raise_exception=True)
        serializer.delete_product_cart()
        return Response({'msg': 'ProductCart deleted successfully.'})
