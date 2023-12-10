from rest_framework.serializers import ModelSerializer
from .models import OrderedProducts, OrderDetails


class OrderedProductsSerializer(ModelSerializer):
    class Meta:
        model = OrderedProducts
        fields = ['product', 'quantity']


class OrderDetailsSerializer(ModelSerializer):
    products = OrderedProductsSerializer(many=True, allow_empty=False, write_only=True)

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = OrderDetails.objects.create(**validated_data)
        for product_data in products_data:
            OrderedProducts.objects.create(
                order=order,
                price=product_data['product'].price,
                **product_data
            )
            OrderDetails.objects.create(phonenumber=validated_data['phonenumber'])
        return order

    class Meta:
        model = OrderDetails
        fields = ['id', 'firstname', 'lastname', 'address', 'phonenumber', 'products']
