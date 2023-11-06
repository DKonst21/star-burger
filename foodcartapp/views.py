import json
import phonenumbers

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, OrderDetails, OrderedProducts


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    try:
        new_order = request.data
        if 'products' not in new_order:
            return Response({'error': 'Key "products" is missing in the request data'},
                            status=status.HTTP_404_NOT_FOUND)

        products = new_order['products']

        for item in products:
            product_id = item.get('product')

            try:
                Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return Response({'error': f'Product with id {product_id} does not exist'},
                                status=status.HTTP_404_NOT_FOUND)

        required_fields = ['products', 'firstname', 'lastname', 'phonenumber', 'address']

        for field in required_fields:
            if field not in new_order or not new_order[field]:
                return Response({'error': f'{field} is required and cannot be empty'},
                                status=status.HTTP_404_NOT_FOUND)

        parsed_number = phonenumbers.parse(new_order['phonenumber'], "RU")
        if not phonenumbers.is_valid_number(parsed_number):
            return Response({'error': 'Products key not presented or not list'},
                            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        defaults = {
            'lastname': new_order.get('lastname', ''),
        }

        order = OrderDetails.objects.get_or_create(firstname=new_order['firstname'],
                                                   phonenumber=new_order['phonenumber'],
                                                   address=new_order['address'],
                                                   defaults=defaults)
        products = Product.objects.all()
        for product in new_order['products']:
            OrderedProducts.objects.create(product=products[product['product']-1],
                                           quantity=product['quantity'],
                                           order=order[0])
        return Response({'message': 'Data successfully processed'})
    except json.JSONDecodeError as e:
        return Response({'error': 'Invalid JSON data', 'details': str(e)})
