from rest_framework import serializers
from django.db.models import Q
from main.models import Animal


class SaveAnimalSerializer(serializers.ModelSerializer):
    category = None
    breed = None

    class Meta:
        model = Animal
        fields = ['category', 'breed', 'image', 'popularity', 'name',
                  'personality', 'likes', 'description', 'posted_by']

    def validate(self, attrs):
        # category_id = attrs.get('category')
        # breed_id = attrs.get('breed')
        # print(category_id.id,breed_id.id,"categ")
        # self.category = Category.objects.filter(id = category_id).first()
        # self.breed = Breed.objects.filter(id = breed_id).first()
        # if self.breed is None:
        #     raise serializers.ValidationError({'msg':{'Breed does not exits'}})

        # if self.category is None:
        #     raise serializers.ValidationError({'msg':{'Category does not exits'}})
        return attrs

    def create(self, validated_data):

        animal = Animal.objects.create(**validated_data)
        return animal


class UpdatePopularitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal,
        fields = ['popularity']

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        instance.popularity = validated_data.get('popularity')
        instance.save()
        return instance


class UpdateAnimalSerializer(serializers.ModelSerializer):
    animal = None
    category = None

    class Meta:
        model = Animal
        fields = ['description', 'category', 'breed', 'image', 'popularity']

    def validate(self, attrs):
        # id = self.context.get('id')
        # categoryId = attrs.get('category_id')
        # name = self.initial_data.get('name')
        # dup_Animal = Animal.objects.filter(~Q(id=id)&Q(name=name)).first()
        # try:
        #     self.animal = Animal.objects.get(id=id)
        #     if self.animal is None:
        #         raise serializers.ValidationError({'msg':'Animal doesn\'t exist.'})
        # except:
        #     raise serializers.ValidationError({'msg':'Animal doesn\'t exist.'})
        # if dup_Animal is not None:
        #     raise serializers.ValidationError({'msg':'Animal with the name already exists.'})
        # categories = Category.objects.filter(id = categoryId)
        # if categories.exists():
        #     self.category = categories.first()
        # else:
        #     raise serializers.ValidationError({'msg':'Please selet a valid category.'})
        return attrs

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image')
        instance.breed = validated_data.get('breed')
        instance.category = validated_data.get('category')
        instance.description = validated_data.get('description')
        instance.save()
        return instance


class DeleteAnimalSerializer(serializers.Serializer):
    animal = None

    def validate(self, attrs):
        id = self.context.get('id')
        try:
            self.animal = Animal.objects.get(
                Q(id=id) & Q(posted_by=self.context.get('user')))
            if self.animal is None:
                raise serializers.ValidationError(
                    {'msg': 'Animal doesn\'t exist.'})
        except:
            raise serializers.ValidationError(
                {'msg': 'Animal doesn\'t exist.'})
        return attrs

    def delete_animal(self):
        name = self.context.get('id')
        self.animal.delete()
