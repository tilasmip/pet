from rest_framework import serializers
from django.db.models import Q
from main.models import ProductCart, Product
from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class SaveProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = ['user','product','quantity']

    def validate(self,attrs):
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
    
    def create(self,validated_data):
        
        product_cart = ProductCart.objects.create(**validated_data)
        return product_cart

class UpdateProductCartSerializer(serializers.ModelSerializer):
    product_cart = None
    category = None
    class Meta:
        model = ProductCart
        fields = ['user','product','quantity']

    def validate(self,attrs):
        
        return attrs
    
    def update(self, instance, validated_data):
        instance.product = validated_data.get('product')
        print("qty",validated_data.get('quantity'))
        instance.quantity = validated_data.get('quantity')
        instance.save()
        return instance

class DeleteProductCartSerializer(serializers.Serializer):
    product_cart = None

    def validate(self,attrs):
        id = self.context.get('id')
        try:
            self.product_cart = ProductCart.objects.get(id=id)
            if self.product_cart is None:
                raise serializers.ValidationError({'msg':'ProductCart doesn\'t exist.'})
        except:
            raise serializers.ValidationError({'msg':'ProductCart doesn\'t exist.'})
        return attrs
    
    def delete_product_cart(self):
        name = self.context.get('id')
        self.product_cart.delete()

        
class GetProductCartSerializer(serializers.Serializer):
    
    def get_queryset(self):
        pageNo = self.data.get('pageNo')
        if pageNo is None or pageNo <=0:
            pageNo = 1

        return ProductCart.objects.all()[(pageNo-1)*10:pageNo*10]