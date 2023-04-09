from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from main.renderers import UserRenderer
from .serializer import (SaveAnimalSerializer,
                         UpdateAnimalSerializer,
                         DeleteAnimalSerializer)
from django.core import serializers
from main.enums import Gender

from main.models import Animal, AnimalWhislist
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class SaveAnimalView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = {
            "popularity": request.data.get("popularity", 0),
            "name": request.data.get("name"),
            "age": request.data.get("age"),
            "gender": request.data.get("gender"),
            "likes": request.data.get("likes"),
            "personality": request.data.get("personality"),
            "category": request.data.get("category"),
            "breed": request.data.get("breed"),
            "image": request.FILES.get("image"),
            "posted_by": request.user.id,
            "description": request.data.get("description"),

        }
        serializer = SaveAnimalSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Success.'}, status=status.HTTP_201_CREATED)


class UpdatePopularityView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        instance = Animal.objects.get(id=pk)
        serializer = UpdateAnimalSerializer(
            instance=instance, data=request.data, context={'id': pk}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Animal updated successfully.'})


class GetRecentAnimalView(generics.ListAPIView):
    parser_classes = []

    def to_object(self, data):
        if (data.image.name is not None):
            name = data.image.name.split("/")[-1]
        else:
            name = ""
        return {
            'description': data.description[:30]+"..." if len(data.description) > 30 else "",
            'breed': data.breed.name,
            "popularity": data.popularity,
            "personality": data.personality,
            "likes": data.likes,
            "name": data.name,
            "age": data.age,
            "gender": data.gender,
            'breed': data.breed.name,
            'image': name,
            'category': data.category.name,
            'id': data.id,
        }
    queryset = Animal.objects.all()

    def get(self, request, format=None):
        renderer_classes = [UserRenderer]

        animals = self.queryset.order_by("-created_at")[:5]
        data = map(self.to_object, animals)

        return Response({'data': data}, status=status.HTTP_200_OK)


class DetailAnimalView(APIView):
    queryset = Animal.objects.all()
    animal_whislist = []

    def get(self, request, id):
        if id is not None:
            data = Animal.objects.filter(id=id).first()
            if request.user.is_authenticated:
                whislist = AnimalWhislist.objects.filter(
                    user=request.user)
                for item in whislist:
                    self.animal_whislist.append(item.animal.id)
            if (data.image.name is not None):
                name = data.image.name.split("/")[-1]
            else:
                name = ""
            result = {
                'description': data.description,
                'breed': data.breed.name,
                "popularity": data.popularity,
                "personality": data.personality,
                "likes": data.likes,
                "name": data.name,
                "age": data.age,
                "gender": data.gender,
                'image': name,
                'category': data.category.name,
                'postedBy': data.posted_by.email,
                'addedDate': data.created_at,
                'id': data.id,
                'love': self.animal_whislist is not None and data.id in self.animal_whislist,
            }
            return Response({'data': result})
        raise serializers.SerializerDoesNotExist()


class GetAnimalView(generics.ListAPIView):
    parser_classes = []
    animal_whislist = []

    def to_object(self, data):
        if (data.image.name is not None):
            name = data.image.name.split("/")[-1]
        else:
            name = ""
        animals = Animal.objects.filter(posted_by=self.request.user)
        return {
            'description': data.description,
            'breed': data.breed.name,
            "popularity": data.popularity,
            "personality": data.personality,
            "likes": data.likes,
            "name": data.name,
            "age": data.age,
            "gender": data.gender,
            'image': name,
            'category': data.category.name,
            'postedBy': data.posted_by.email,
            'addedDate': data.created_at,
            'id': data.id,
            'deletable': True if data in animals else False,
            'love': self.animal_whislist is not None and data.id in self.animal_whislist,
        }

    def purify(self, value):
        if value is not None:
            value = value.strip()
        return value or None

    def get_queryset(self, request):
        animals = Animal.objects.all()
        breed = self.purify(request.GET.get('breed'))
        if breed is not None:
            animals = animals.filter(breed__id=breed)

        category = self.purify(request.GET.get('category'))
        if category is not None:
            animals = animals.filter(category__id=category)

        age = self.purify(request.GET.get('age'))
        if age is not None:
            age = int(age)
            if age > 0 and age <= 6:
                match age:
                    case 1:
                        animals = animals.filter(age__lte=3)
                    case 2:
                        animals = animals.filter(age__lte=6)
                    case 3:
                        animals = animals.filter(age__lte=9)
                    case 4:
                        animals = animals.filter(age__lte=12)
                    case 5:
                        animals = animals.filter(age__lte=15)
                    case 6:
                        animals = animals.filter(age__gte=15)

        gender = self.purify(request.GET.get('gender'))
        if gender is not None and gender != "0":
            gender = getattr(Gender, gender.strip())
            animals = animals.filter(gender=gender)
            print(len(animals), gender)
        search = self.purify(request.GET.get('search'))
        if search is not None:
            animals = animals.filter(name__icontains=search)

        pouplarity = self.purify(request.GET.get('popularity'))
        if pouplarity == 2 or pouplarity == 1:
            if pouplarity == 2:
                animals = animals.order_by("popularity") or None
            else:
                animals = animals.order_by("-popularity") or None

        pageNo = self.purify(request.GET.get('pageNo'))

        if pageNo is None or pageNo <= 0:
            pageNo = 1
        animals = animals[(pageNo-1)*10:pageNo*10]
        return animals

    def get(self, request, format=None):
        renderer_classes = [UserRenderer]
        if request.user.is_authenticated:
            whislist = AnimalWhislist.objects.filter(
                user=request.user)
            for item in whislist:
                self.animal_whislist.append(item.animal.id)
        data = map(self.to_object, self.get_queryset(request))

        return Response({'data': data}, status=status.HTTP_200_OK)


class UpdateAnimalView(APIView):
    queryset = Animal.objects.all()
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, format=None):
        instance = Animal.objects.get(id=pk)
        serializer = UpdateAnimalSerializer(
            instance=instance, data=request.data, context={'id': pk}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Animal updated successfully.'})


class DeleteAnimalView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        serializer = DeleteAnimalSerializer(
            data=request.data, context={'id': pk, 'user': request.user})
        serializer.is_valid(raise_exception=True)
        try:
            serializer.delete_animal()
        except Exception.RestrictedError as E:
            return Response({'msg': 'Unable to delete please contact admin.'}, status=status.HTTP_424_FAILED_DEPENDENCY)
        return Response({'msg': 'Animal deleted successfully.'})
