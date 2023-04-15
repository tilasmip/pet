from rest_framework import serializers
from django.db.models import Q
from main.models import AnimalWishlist


class SaveAnimalWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalWishlist
        fields = ['user', 'animal']

    def validate(self, attrs):
        animal = AnimalWishlist.objects.filter(
            Q(animal=attrs.get('animal')) & Q(user=attrs.get('user'))).first()
        if animal is not None:
            raise serializers.ValidationError(
                {'msg': 'Animal already in wishlist.'})
        return attrs

    def create(self, validated_data):
        animal = validated_data.get('animal')
        animal.popularity += 1
        animal.save()
        animal_wishlist = AnimalWishlist.objects.create(**validated_data)
        return animal_wishlist


class DeleteAnimalWishlistSerializer(serializers.Serializer):
    animal_wishlist = None

    def validate(self, attrs):
        id = self.context.get('id')
        try:
            self.animal_wishlist = AnimalWishlist.objects.get(
                Q(id=id) & Q(user=self.context.get('user')))
            if self.animal_wishlist is None:
                raise serializers.ValidationError(
                    {'msg': 'AnimalWishlist doesn\'t exist.'})
        except:
            raise serializers.ValidationError(
                {'msg': 'AnimalWishlist doesn\'t exist.'})
        return attrs

    def delete_animal_wishlist(self):
        self.animal_wishlist.delete()


class GetAnimalWishlistSerializer(serializers.Serializer):

    def get_queryset(self):
        return AnimalWishlist.objects.filter(user=self.context.get('user'))
