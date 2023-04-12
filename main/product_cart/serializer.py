from rest_framework import serializers
from django.db.models import Q
from main.models import ProductCart, CartSummary


class SaveProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCart
        fields = ['product', 'quantity', 'rate']

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):

        user = self.context.get('user')
        print(user, "use")
        summaryList = CartSummary.objects.filter(Q(user=user) & Q(sold=False))
        if not summaryList.exists():
            summary = CartSummary(user=user, sold=False)
            summary.save()
        else:
            summary = summaryList[0]

        product_carts = ProductCart.objects.filter(
            product=validated_data.get('product'), cart_summary__user=user, cart_summary__sold=False)
        if product_carts.exists():
            return product_carts[0]
        else:
            product_cart = ProductCart.objects.create(
                cart_summary=summary, rate=validated_data.get('product').price, **validated_data)
            return product_cart


# class SaveCartSummarySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartSummary
#         fields = ['user', 'amount', 'shipping_address',
#                   'additional_info', 'processing']

#     def validate(self, attrs):
#         return attrs

#     def create(self, validated_data):
#         carts = ProductCart.objects.filter(user=validated_data.get('user'))
#         if carts.exists():
#             summary = CartSummary.objects.create(**validated_data)
#             for cart in carts:
#                 cart.cart_summary = summary
#                 cart.save()
#             return summary
#         raise serializers.ValidationError("No Item found.")
class ProceedPaymentSerilizer(serializers.ModelSerializer):
    class Meta:
        model = CartSummary
        fields = ('shipping_address', 'additional_info')

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CompletePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartSummary
        fields = ('reference_id', 'sold')

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PurchaseInvoiceSerializer(serializers.Serializer):

    def get_queryset(self):
        user_id = self.context.get('user')
        id = self.context.get('id')
        print(user_id, id)
        try:
            summary = CartSummary.objects.get(
                user__id=user_id, sold=True, id=id)
            return summary.cart_details()
        except CartSummary.DoesNotExist:
            raise serializers.ValidationError({'msg': 'Not found'})
# class UpdateProductCartSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = ProductCart
#         fields = ['user', 'product', 'quantity']

#     def validate(self, attrs):

#         return attrs

#     def update(self, instance, validated_data):
#         instance.product = validated_data.get('product')
#         instance.quantity = validated_data.get('quantity')
#         instance.rate = instance.product.rate
#         instance.save()
#         return instance


class DeleteProductCartSerializer(serializers.Serializer):
    product_cart = None

    def validate(self, attrs):
        id = self.context.get('id')
        try:
            self.product_cart = ProductCart.objects.get(id=id)
            if self.product_cart is None:
                raise serializers.ValidationError(
                    {'msg': 'ProductCart doesn\'t exist.'})
        except:
            raise serializers.ValidationError(
                {'msg': 'ProductCart doesn\'t exist.'})
        return attrs

    def delete_product_cart(self):
        name = self.context.get('id')
        self.product_cart.delete()


class GetProductCartSerializer(serializers.Serializer):

    def get_queryset(self):
        user_id = self.context.get('user')
        summaryList = CartSummary.objects.filter(user__id=user_id, sold=False)
        summary = summaryList[0]
        if len(summary) > 1:
            summaryList[1:].delete()
        return summary.cart_details()
