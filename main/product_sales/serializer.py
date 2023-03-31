from rest_framework import serializers
from django.db.models import Q
from main.models import ProductSales, Product
from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class SaveProductSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSales
        fields = ['user','product','quantity','amount','cupon_id','referenceId']

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
        
        product_sales = ProductSales.objects.create(**validated_data)
        return product_sales

# class UpdateProductSalesSerializer(serializers.ModelSerializer):
#     product_sales = None
#     category = None
#     class Meta:
#         model = ProductSales
#         fields = ['user','product','quantity']

#     def validate(self,attrs):
        
#         return attrs
    
#     def update(self, instance, validated_data):
#         instance.product = validated_data.get('product')
#         print("qty",validated_data.get('quantity'))
#         instance.quantity = validated_data.get('quantity')
#         instance.save()
#         return instance

# class DeleteProductSalesSerializer(serializers.Serializer):
#     product_sales = None

#     def validate(self,attrs):
#         id = self.context.get('id')
#         try:
#             self.product_sales = ProductSales.objects.get(id=id)
#             if self.product_sales is None:
#                 raise serializers.ValidationError({'msg':'ProductSales doesn\'t exist.'})
#         except:
#             raise serializers.ValidationError({'msg':'ProductSales doesn\'t exist.'})
#         return attrs
    
#     def delete_product_sales(self):
#         name = self.context.get('id')
#         self.product_sales.delete()

        
class GetProductSalesSerializer(serializers.Serializer):
    
    def get_queryset(self):
        pageNo = self.data.get('pageNo')
        if pageNo is None or pageNo <=0:
            pageNo = 1

        return ProductSales.objects.all()[(pageNo-1)*10:pageNo*10]