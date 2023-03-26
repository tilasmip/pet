from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from main.renderers import UserRenderer
from .serializer import (SaveProductSerializer, GetProductSerializer)


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
class SaveProductView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes=[IsAuthenticated, IsAdminUser]
    def post(self,request, format=None):
        serializer = SaveProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create_product()
        serializer.save()
        return Response({'msg':'Success.'},status = status.HTTP_201_CREATED)

class GetProductView(APIView):
    def get(self,request,format=None):
        renderer_classes = [UserRenderer]
        serializer = GetProductSerializer(data= request.data)
        serializer.is_valid(raise_exception= True)
        data = serializer.get_queryset()
        return Response({'data':data},status = status.HTTP_200_OK)