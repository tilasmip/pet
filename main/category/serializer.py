from rest_framework import serializers
from django.db.models import Q
from main.models import Category


class SaveCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def validate(self, attrs):
        return attrs

    def create_Category(self):
        name = self.data.get('name')
        category = Category(name=name)
        category.save()


class UpdateCategorySerializer(serializers.ModelSerializer):
    category = None

    class Meta:
        model = Category
        fields = ['name']

    def validate(self, attrs):
        id = self.context.get('id')
        name = self.initial_data.get('name')
        dup_category = Category.objects.filter(
            ~Q(id=id) & Q(name=name)).first()
        if dup_category is not None:
            raise serializers.ValidationError(
                {'msg': 'Category with the name already exists.'})
        try:
            self.category = Category.objects.get(id=id)
            if self.category is None:
                raise serializers.ValidationError(
                    {'msg': 'Category doesn\'t exist.'})
        except:
            raise serializers.ValidationError(
                {'msg': 'Category doesn\'t exist.'})
        return attrs

    def update_category(self):
        name = self.validated_data.get('name')
        self.category.name = name
        self.category.save()


class DeleteCategorySerializer(serializers.Serializer):
    category = None

    def validate(self, attrs):
        id = self.context.get('id')
        try:
            self.category = Category.objects.get(id=id)
            if self.category is None:
                raise serializers.ValidationError(
                    {'msg': 'Category doesn\'t exist.'})
        except:
            raise serializers.ValidationError(
                {'msg': 'Category doesn\'t exist.'})
        return attrs

    def delete_category(self):
        name = self.context.get('id')
        self.category.delete()


class GetCategorySerializer(serializers.Serializer):

    def get_queryset(self):

        return Category.objects.all()
