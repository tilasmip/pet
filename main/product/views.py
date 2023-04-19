from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (
    GetProductSerializer,
    RecentProductSerializer
)
from django.core import serializers
import math
from main.models import Product
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# class SaveProductView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes=[IsAuthenticated,IsAdminUser]
#     def post(self,request, format=None):
#         data = {
#             "name": request.data.get("name"),
#             "category":request.data.get("category_id"),
#             "description":request.data.get("description"),
#             "image":request.FILES.get("image"),
#             "price":request.data.get('price'),
#             'stock':request.data.get('stock'),
#         }
#         serializer = SaveProductSerializer(data = data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'msg':'Success.'},status = status.HTTP_201_CREATED)


class RecentProductView(APIView):
    serializer_class = RecentProductSerializer

    def to_object(self, data):
        if (data.image.name is not None):
            name = data.image.name.split("/")[-1]
        else:
            name = ""
        return {
            'description': data.description,
            'name': data.name,
            'price': data.price,
            'image': name,
            'category': data.category.name,
            'category_id': data.category.id,
            'id': data.id,
            'stock': data.stock
        }

    queryset = Product.objects.all()

    def get(self, request, format=None):
        renderer_classes = [UserRenderer]
        serializer = RecentProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = map(self.to_object, self.queryset.all())

        return Response({'data': data}, status=status.HTTP_200_OK)


class GetProductView(generics.ListAPIView):
    parser_classes = []

    def to_object(self, data):
        if (data.image.name is not None):
            name = data.image.name.split("/")[-1]
        else:
            name = ""
        return {
            'description': data.description,
            'name': data.name,
            'price': data.price,
            'image': name,
            'category': data.category.name,
            'category_id': data.category.id,
            'id': data.id,
            'stock': data.stock
        }

    def get(self, request, format=None):
        renderer_classes = [UserRenderer]
        name = request.query_params.get('name')
        pageNo = request.query_params.get('pageNo')
        category = request.query_params.get('category')
        order = request.query_params.get('order') == '1'
        print(name, "name", pageNo, "pageNo",
              category, "cat", order, "Filter data")
        totalPage = 1
        if pageNo is None:
            pageNo = 1
        else:
            pageNo = int(pageNo)
        products = Product.objects.all()
        if (name is not None and name != ""):
            products = products.filter(name__icontains=name)
        if (category is not None and category != "0" and category != ""):
            products = products.filter(category__id=category)
            totalPage = math.floor(len(products)/5)
        if (order is not None and order != "0" and order != ""):
            products = products.order_by(
                '-price' if order == True else "price")[(pageNo-1)*pageNo:pageNo*5]
        data = map(self.to_object, products)

        return Response({'data': data, 'total': totalPage}, status=status.HTTP_200_OK)

# class UpdateProductView(APIView):
#     queryset = Product.objects.all()
#     renderer_classes = [UserRenderer]
#     permission_classes=[IsAuthenticated,IsAdminUser]
#     def put(self,request,pk,format = None):
#         instance = Product.objects.get(id=pk)
#         serializer = UpdateProductSerializer(instance = instance, data = request.data, context = {'id':pk}, partial = True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'msg':'Product updated successfully.'})

# class DeleteProductView(APIView):
#     renderer_classes = [UserRenderer]
#     permission_classes=[IsAuthenticated, IsAdminUser]
#     def delete(self,request,pk,format = None):
#         serializer = DeleteProductSerializer(data = request.data, context = {'id':pk})
#         serializer.is_valid(raise_exception=True)
#         serializer.delete_product()
#         return Response({'msg':'Product deleted successfully.'})
