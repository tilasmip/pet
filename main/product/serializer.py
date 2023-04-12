from rest_framework import serializers
from main.models import Product, Product


class RecentProductSerializer(serializers.Serializer):
    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")[:5]


class GetProductSerializer(serializers.Serializer):

    def get_queryset(self):
        name = self.context.get('name')
        pageNo = self.context.get('pageNo')
        category = self.context.get('category')
        order = self.context.get('order') == '1'
        if pageNo is None:
            pageNo = 1
        products = Product.objects.all()
        if (name is not None and name != ""):
            products.filter(name__contains=name)
        if (category is not None and category != "0" and category != ""):
            products = products.filter(category__id=category)
        if (order is not None and order != "0" and order != ""):
            products = products.order_by(
                '-price' if order == "1" else "price")[:5]

        return products[(pageNo-1)*10:pageNo*10]
