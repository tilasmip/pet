from rest_framework import serializers
from django.db.models import Q
from main.models import Product, ProductCart, ProductSales,ProductWhislist, Category
from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class SaveProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','image','category','stock','price']

    def validate(self,attrs):
        return attrs
    
    def create_product(self):
        name = self.data.get('name')
        category_id = self.data.get('category_id')
        categories = Category.objects.filter(id = category_id)
        if category.exists():
            category = categories[0]
        price = self.data.get('price')
        stock = self.data.get('stock')
        product = Product(name = name, category = category, price = price, stock = stock)
        product.save()

        
class GetProductSerializer(serializers.Serializer):
    class Meta:
        model = Product
        fields = ['name','image','category','stock','price']
    
    def get_queryset(self):
        name = self.data.get('name')
        category_id = self.data.get('category_id')
        return Product.objects.filter(name= name, category__id = category_id)
