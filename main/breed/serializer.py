from rest_framework import serializers
from django.db.models import Q
from main.models import Breed, Category


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


class SaveBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ('name', 'category',)

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        print("creawteing")
        return super().create(**validated_data)


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
        breeds = Breed.objects.all()
        category = self.context.get('category')
        print("Category", category)
        if category is not None and category != "":
            breeds = breeds.filter(category__id=category)
        return breeds
