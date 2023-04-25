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
        fields = ['description', 'category', 'breed', 'likes',
                  'personality', 'gender', 'age', 'name', 'approve_post',]

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
       return super().update(instance, validated_data)


class ApprovePostAnimalSerializer(serializers.ModelSerializer):
    animal = None
    category = None

    class Meta:
        model = Animal
        fields = ['approve_post']

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        instance.approve_post = validated_data.get('approve_post')
        instance.save()
        return instance


class ApproveAdoptionSerializer(serializers.ModelSerializer):
    animal = None
    category = None

    class Meta:
        model = Animal
        fields = ['adopted']

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        instance.adopted = validated_data.get('adopted')
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
