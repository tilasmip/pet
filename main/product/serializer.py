from rest_framework import serializers
from django.db.models import Q
from main.models import Product, Category,Breed, ProductWhislist,ProductWhislist, Product
from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class SaveProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['category','description','image','name','price','stock']

    def validate(self,attrs):
        return attrs
    
    def create(self,validated_data):
        
        product = Product.objects.create(**validated_data)
        return product

class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['description','category','image','name','price','stock']

    def validate(self,attrs):
        # id = self.context.get('id')
        # categoryId = attrs.get('category_id')
        # name = self.initial_data.get('name')
        # dup_Product = Product.objects.filter(~Q(id=id)&Q(name=name)).first()
        # try:
        #     self.product = Product.objects.get(id=id)
        #     if self.product is None:
        #         raise serializers.ValidationError({'msg':'Product doesn\'t exist.'})
        # except:
        #     raise serializers.ValidationError({'msg':'Product doesn\'t exist.'})
        # if dup_Product is not None:
        #     raise serializers.ValidationError({'msg':'Product with the name already exists.'})
        # categories = Category.objects.filter(id = categoryId)
        # if categories.exists():
        #     self.category = categories.first()
        # else:
        #     raise serializers.ValidationError({'msg':'Please selet a valid category.'})
        return attrs
    
    def update(self, instance, validated_data):
        instance.imaage = validated_data.get('image')
        instance.breed = validated_data.get('breed')
        instance.category = validated_data.get('category')
        instance.description = validated_data.get('description')
        instance.save()
        return instance

class DeleteProductSerializer(serializers.Serializer):
    product = None

    def validate(self,attrs):
        id = self.context.get('id')
        try:
            self.product = Product.objects.get(id=id)
            if self.product is None:
                raise serializers.ValidationError({'msg':'Product doesn\'t exist.'})
        except:
            raise serializers.ValidationError({'msg':'Product doesn\'t exist.'})
        return attrs
    
    def delete_product(self):
        name = self.context.get('id')
        self.product.delete()

        
class GetProductSerializer(serializers.Serializer):
    
    def get_queryset(self):
        pageNo = self.data.get('pageNo')
        if pageNo is None or pageNo <=0:
            pageNo = 1

        return Product.objects.all()[(pageNo-1)*10:pageNo*10]