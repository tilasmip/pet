from rest_framework import serializers
from django.db.models import Q
from main.models import ProductWhislist, ProductWhislist, ProductWhislist


class SaveProductWhislistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductWhislist
        fields = ['user', 'product']

    def validate(self, attrs):
        product = ProductWhislist.objects.filter(
            Q(product=attrs.get('product')) & Q(user=attrs.get('user'))).first()
        if product is not None:
            raise serializers.ValidationError(
                {'msg': {'Product already in whislist.'}})
        return attrs

    def create(self, validated_data):

        product_whislist = ProductWhislist.objects.create(**validated_data)
        return product_whislist


class DeleteProductWhislistSerializer(serializers.Serializer):
    product_whislist = None

    def validate(self, attrs):
        id = self.context.get('id')
        try:
            self.product_whislist = ProductWhislist.objects.get(
                Q(id=id) & Q(user=self.context.get('user')))
            if self.product_whislist is None:
                raise serializers.ValidationError(
                    {'msg': 'ProductWhislist doesn\'t exist.'})
        except:
            raise serializers.ValidationError(
                {'msg': 'ProductWhislist doesn\'t exist.'})
        return attrs

    def delete_product_whislist(self):
        self.product_whislist.delete()


class GetProductWhislistSerializer(serializers.Serializer):

    def get_queryset(self):
        pageNo = self.data.get('pageNo')
        if pageNo is None or pageNo <= 0:
            pageNo = 1

        return ProductWhislist.objects.all()[(pageNo-1)*10:pageNo*10]
