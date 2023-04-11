from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveProductSalesSerializer)
from django.core import serializers
import math

from main.models import ProductSales, ProductCart, CartSummary, Product
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class SaveProductSalesView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        summaryId = request.data.get("cartSummaryId")
        if (summaryId is None):
            return Response({'msg': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
        summary = CartSummary.objects.filter(id=summaryId).first()
        if (summary is None):
            return Response({'msg': 'Invalid request. No summary'}, status=status.HTTP_400_BAD_REQUEST)
        refId = request.data.get("referenceId")
        carts = ProductCart.objects.filter(cart_summary=summary)
        for cart in carts:
            data = {
                "user": request.user.id,
                "product": cart.product.pk,
                "quantity": cart.quantity,
                "amount": round(cart.product.price * cart.quantity, 2),
                "referenceId": refId
            }
            print(data.get("amount"), "amt")
            serializer = SaveProductSalesSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            result = []
            result.append({
                "amount": round(cart.quantity * cart.product.price),
                "name": cart.product.name
            })
            qty = cart.product.stock
            if (qty-cart.quantity > 0):
                cart.product.stock -= cart.quantity
                cart.product.save()
            cart.delete()

        return Response({'data': refId}, status=status.HTTP_201_CREATED)


class GetProductSalesView(generics.ListAPIView):
    parser_classes = []
    permission_classes = [IsAuthenticated]
    queryset = ProductSales.objects.all()

    def to_object(self, data):
        return {
            'user_id': data.user.id,
            'user': data.user.name,
            'product_id': data.product.id,
            'product': data.product.name,
            'amount': data.amount,
            'quantity': data.quantity,
            'id': data.id
        }

    def get(self, request, refId, format=None):
        renderer_classes = [UserRenderer]

        data = map(self.to_object, self.queryset.filter(referenceId=refId))
        return Response({'data': data, 'username': request.user.name}, status=status.HTTP_200_OK)

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
