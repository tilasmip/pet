from rest_framework import serializers
from django.db.models import Q
from main.models import ProductWishlist, ProductWishlist, ProductWishlist


class SaveProductWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductWishlist
        fields = ['user', 'product']

    def validate(self, attrs):
        product = ProductWishlist.objects.filter(
            Q(product=attrs.get('product')) & Q(user=attrs.get('user'))).first()
        if product is not None:
            raise serializers.ValidationError(
                {'msg': {'Product already in wishlist.'}})
        return attrs

    def create(self, validated_data):

        product_wishlist = ProductWishlist.objects.create(**validated_data)
        return product_wishlist


class DeleteProductWishlistSerializer(serializers.Serializer):
    product_wishlist = None

    def validate(self, attrs):
        id = self.context.get('id')
        try:
            self.product_wishlist = ProductWishlist.objects.get(
                Q(id=id) & Q(user=self.context.get('user')))
            if self.product_wishlist is None:
                raise serializers.ValidationError(
                    {'msg': 'ProductWishlist doesn\'t exist.'})
        except:
            raise serializers.ValidationError(
                {'msg': 'ProductWishlist doesn\'t exist.'})
        return attrs

    def delete_product_wishlist(self):
        self.product_wishlist.delete()


class GetProductWishlistSerializer(serializers.Serializer):

    def get_queryset(self):
        pageNo = self.data.get('pageNo')
        if pageNo is None or pageNo <= 0:
            pageNo = 1

        return ProductWishlist.objects.all()[(pageNo-1)*10:pageNo*10]
