from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveProductWhislistSerializer,
                         GetProductWhislistSerializer,
                         DeleteProductWhislistSerializer)
from rest_framework.permissions import IsAuthenticated


class SaveProductWhislistView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = {
            "user": request.user.id,
            "product": request.data.get("product_id"),
        }
        serializer = SaveProductWhislistSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Success.'}, status=status.HTTP_201_CREATED)


class GetProductWhislistView(generics.ListAPIView):
    parser_classes = []

    def to_object(self, data):
        return {
            'product_id': data.product.id,
            'product': data.product.breed.name,
            'product': data.product.description,
            'id': data.id
        }

    def get(self, request, format=None):
        renderer_classes = [UserRenderer]
        serializer = GetProductWhislistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object, serializer.get_queryset())

        return Response({'data': data}, status=status.HTTP_200_OK)


class DeleteProductWhislistView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        serializer = DeleteProductWhislistSerializer(
            data=request.data, context={'id': pk, 'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.delete_product_whislist()
        return Response({'msg': 'ProductWhislist deleted successfully.'})
