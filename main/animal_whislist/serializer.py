from rest_framework import serializers
from django.db.models import Q
from main.models import AnimalWhislist, Category, Breed, Animal, AnimalWhislist, Product
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class SaveAnimalWhislistSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalWhislist
        fields = ['user', 'animal']

    def validate(self, attrs):
        animal = AnimalWhislist.objects.filter(
            Q(animal=attrs.get('animal')) & Q(user=attrs.get('user'))).first()
        if animal is not None:
            raise serializers.ValidationError(
                {'msg': 'Animal already in whislist.'})
        return attrs

    def create(self, validated_data):
        animal = validated_data.get('animal')
        animal.popularity += 1
        animal.save()
        animal_whislist = AnimalWhislist.objects.create(**validated_data)
        return animal_whislist


class DeleteAnimalWhislistSerializer(serializers.Serializer):
    animal_whislist = None

    def validate(self, attrs):
        id = self.context.get('id')
        try:
            self.animal_whislist = AnimalWhislist.objects.get(
                Q(id=id) & Q(user=self.context.get('user')))
            if self.animal_whislist is None:
                raise serializers.ValidationError(
                    {'msg': 'AnimalWhislist doesn\'t exist.'})
        except:
            raise serializers.ValidationError(
                {'msg': 'AnimalWhislist doesn\'t exist.'})
        return attrs

    def delete_animal_whislist(self):
        self.animal_whislist.delete()


class GetAnimalWhislistSerializer(serializers.Serializer):

    def get_queryset(self):
        return AnimalWhislist.objects.all()
