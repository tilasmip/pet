from rest_framework import serializers
from django.db.models import Q
from main.models import Breed, Category


class SaveBreedSerializer(serializers.ModelSerializer):
    category = None
    category_id = serializers.IntegerField(required=True)

    class Meta:
        model = Breed
        fields = ['name', 'category_id']

    def validate(self, attrs):
        category_id = attrs.get('category_id')
        self.category = Category.objects.filter(id=category_id).first()
        if self.category is None:
            raise serializers.ValidationError(
                {'msg': {'Category does not exits'}})
        return attrs

    def create_Breed(self):
        name = self.validated_data.get('name')

        breed = Breed(name=name, category=self.category)
        breed.save()


class UpdateBreedSerializer(serializers.ModelSerializer):
    breed = None
    category = None
    category_id = serializers.IntegerField(required=True)

    class Meta:
        model = Breed
        fields = ['name', 'category_id']

    def validate(self, attrs):
        id = self.context.get('id')
        categoryId = attrs.get('category_id')
        name = self.initial_data.get('name')
        dup_Breed = Breed.objects.filter(~Q(id=id) & Q(name=name)).first()
        try:
            self.breed = Breed.objects.get(id=id)
            if self.breed is None:
                raise serializers.ValidationError(
                    {'msg': 'Breed doesn\'t exist.'})
        except:
            raise serializers.ValidationError({'msg': 'Breed doesn\'t exist.'})
        if dup_Breed is not None:
            raise serializers.ValidationError(
                {'msg': 'Breed with the name already exists.'})
        categories = Category.objects.filter(id=categoryId)
        if categories.exists():
            self.category = categories.first()
        else:
            raise serializers.ValidationError(
                {'msg': 'Please selet a valid category.'})
        return attrs

    def update_breed(self):
        name = self.validated_data.get('name')
        self.breed.category = self.category
        self.breed.name = name
        self.breed.save()


class DeleteBreedSerializer(serializers.Serializer):
    breed = None

    def validate(self, attrs):
        id = self.context.get('id')
        try:
            self.breed = Breed.objects.get(id=id)
            if self.breed is None:
                raise serializers.ValidationError(
                    {'msg': 'Breed doesn\'t exist.'})
        except:
            raise serializers.ValidationError({'msg': 'Breed doesn\'t exist.'})
        return attrs

    def delete_breed(self):
        name = self.context.get('id')
        self.breed.delete()


class GetBreedSerializer(serializers.Serializer):

    def get_queryset(self):
        pageNo = self.data.get('pageNo')
        if pageNo is None or pageNo <= 0:
            pageNo = 1

        return Breed.objects.all()[(pageNo-1)*10:pageNo*10]
