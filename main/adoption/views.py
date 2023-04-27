from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveAdoptionSerializer,
                         DeleteAdoptionSerializer,
                         RejectAdoptionSerializer,
                         AcceptAdoptionSerializer,
                         UpdateAdoptionSerializer)
from django.core import serializers

from main.models import Adoption
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from main.enums import AdoptionStatus


class SaveAdoptionView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = {
            "animal": request.data.get("animal_id"),
            "message": request.data.get("message"),
            "status": "PENDING",
            "requested_by": request.user.id

        }
        serializer = SaveAdoptionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Success.'}, status=status.HTTP_201_CREATED)


class GetAdoptionView(APIView):
    queryset = Adoption.objects.all()
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def to_object(self, data):
        result = {
            'id': data.id,
            'name': data.animal.name,
            'requestedBy': data.requested_by.email,
            'requestDate': str(data.created_at),
            'status':data.status,
            'message': data.message
        }
        return result

    def get(self, request, format=None):
        requestList = []
        for request in self.queryset.order_by("-status"):
            requestList.append(self.to_object(request))
        return Response({'data': requestList})


class RejectdoptionView(APIView):
    queryset = Adoption.objects.all()
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, pk, format=None):
        instance = Adoption.objects.get(id=pk)
        serializer = RejectAdoptionSerializer(
            instance=instance, data={id: pk}, context={'id': pk, 'user': request.user}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': 'Adoption rejected successfully.'})


class AcceptdoptionView(APIView):
    queryset = Adoption.objects.all()
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, pk, format=None):
        instance = Adoption.objects.get(id=pk)
        serializer = AcceptAdoptionSerializer(
            instance=instance, data={'id': pk}, context={'id': pk, 'user': request.user}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data': 'Adoption accepted successfully.'})


class UpdateAdoptionView(APIView):
    queryset = Adoption.objects.all()
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        instance = Adoption.objects.get(id=pk)
        serializer = UpdateAdoptionSerializer(
            instance=instance, data=request.data, context={'id': pk, 'user': request.user}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Adoption updated successfully.'})


class DeleteAdoptionView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        serializer = DeleteAdoptionSerializer(
            data=request.data, context={'id': pk, 'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.delete_animal()
        return Response({'msg': 'Animal deleted successfully.'})
