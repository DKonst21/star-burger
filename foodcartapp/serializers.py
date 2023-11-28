from rest_framework.serializers import ModelSerializer
from .models import OrderedProducts, OrderDetails


class OrderedProductsSerializer(ModelSerializer):
    class Meta:
        model = OrderedProducts
        fields = ['product', 'quantity']


class OrderDetailsSerializer(ModelSerializer):
    products = OrderedProductsSerializer(many=True, allow_empty=False, write_only=True)

    class Meta:
        model = OrderDetails
        fields = ['id', 'firstname', 'lastname', 'address', 'phonenumber', 'products']
