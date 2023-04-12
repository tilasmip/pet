from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveProductCartSerializer,
                         GetProductCartSerializer,
                         CompletePaymentSerializer,
                         DeleteProductCartSerializer,
                         PurchaseInvoiceSerializer,
                         ProceedPaymentSerilizer)
from django.db.models import Q
import json
from main.models import ProductCart, CartSummary
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class SaveProductCartView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        data = {
            "product": request.data.get("product_id"),
            "quantity": request.data.get("quantity", 1),
        }
        serializer = SaveProductCartSerializer(
            data=data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Success.'}, status=status.HTTP_201_CREATED)


class ProceedPaymentView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        data = {
            "shipping_address": request.data.get("shipping_address"),
            "additional_info": request.data.get("additional_info"),
        }
        cart_data = request.data.get('cart_data')
        if (cart_data is None):
            return Response({'msg': 'No cart data found.'}, status=status.HTTP_400_BAD_REQUEST)

        instance = CartSummary.objects.get(
            id=pk, sold=False, user=request.user)
        serializer = ProceedPaymentSerilizer(
            instance=instance, data=data, context={'id': pk}, partial=True)
        serializer.is_valid(raise_exception=True)
        for cart in cart_data:
            cart_id = cart.get('id')
            cart_rate = cart.get('rate')
            cart_quantity = cart.get('quantity')
            item = ProductCart.objects.filter(Q(id=cart_id)).first()
            if item is not None:
                item.rate = cart_rate
                item.quantity = cart_quantity
                item.save()
        serializer.save()

        return Response({'msg': 'Shipping address updated successfully.'})


class CompletePaymentView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        summary = CartSummary.objects.filter(
            Q(id=pk) & Q(sold=False)).first()
        if (summary is None):
            return Response({'msg': 'Invalid request. No summary'}, status=status.HTTP_400_BAD_REQUEST)
        refId = request.data.get("referenceId")
        data = {
            "reference_id": refId,
            "sold": True
        }
        serializer = CompletePaymentSerializer(
            data=data, instance=summary, partial=True)
        serializer.is_valid(raise_exception=True)
        for item in summary.cart_details():
            item.product.stock -= item.quantity
            item.product.save()
        serializer.save()
        return Response({'data': summary.id})


class PurchaseInvoiceView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def to_object(self, data):
        return {
            'user': self.request.user.name,
            'product': data.product.name,
            'amount': str((data.quantity * data.rate)),
            'rate': str(data.rate),
            'quantity': str(data.quantity),
            'id': str(data.id)
        }

    def get(self, request, id, format=None):
        renderer_classes = [UserRenderer]
        permission_classes = [IsAuthenticated]
        serializer = PurchaseInvoiceSerializer(
            data=request.data, context={'user': request.user.id, 'id': id})
        serializer.is_valid(raise_exception=True)
        data = []
        out = serializer.get_queryset()
        for item in out:
            data.append(self.to_object(item))

        return Response({'data': data}, status=status.HTTP_200_OK)


class GetProductCartView(generics.ListAPIView):
    parser_classes = []

    def to_object(self, data):
        if (data.product.image is not None):
            name = data.product.image.name.split("/")[-1]
        else:
            name = ""
        print(data.product.image)
        return {
            'user_id': self.request.user.id,
            'user': self.request.user.name,
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
        user = request.user
        # id = request.data.get('id')
        summary = CartSummary.objects.filter(
            Q(user=user) & Q(sold=False)).first()
        if summary is None:
            return Response({'data': []}, status=status.HTTP_200_OK)

        data = map(self.to_object, summary.cart_details())

        return Response({'data': data, 'id': summary.id}, status=status.HTTP_200_OK)


# class UpdateProductCartView(APIView):
#     queryset = ProductCart.objects.all()
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]

#     def put(self, request, pk, format=None):
#         instance = ProductCart.objects.get(id=pk)
#         serializer = UpdateProductCartSerializer(
#             instance=instance, data=request.data, context={'id': pk}, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'msg': 'ProductCart updated successfully.'})


class DeleteProductCartView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, pk, format=None):
        serializer = DeleteProductCartSerializer(
            data=request.data, context={'id': pk})
        serializer.is_valid(raise_exception=True)
        serializer.delete_product_cart()
        return Response({'msg': 'ProductCart deleted successfully.'})
