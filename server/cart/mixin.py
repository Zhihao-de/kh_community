from rest_framework import status
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.settings import api_settings

from cart.models import CartModel
from cart.serializers import CartSerializer
from products.models import ProductModel
from users.models import UserModel


class CartPatchModelMixin(UpdateModelMixin):
    """
    Patch a model instance.
    """

    def patch(self, request, *args, **kwargs):
        product_id = request.data.pop("product")
        product = ProductModel.objects.get(id=product_id)
        quantity = request.data.pop("quantity")
        cart_id = request.data.pop("id")
        updated_cart = CartModel.objects.get(id=cart_id)
        updated_cart.quantity = quantity
        updated_cart.product = product
        updated_cart.save()
        headers = self.get_success_headers(CartSerializer(updated_cart).data)

        return Response(CartSerializer(updated_cart).data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class CartCreateModelMixin(CreateModelMixin):
    """
    Create a model instance.
    """

    def batch_create(self, request, *args, **kwargs):
        product_id = request.data.pop("product")
        product = ProductModel.objects.get(id=product_id)
        user_id = request.data.pop("user")
        user = UserModel.objects.get(id=user_id)
        quantity = request.data.pop("quantity")
        created_cart = CartModel.objects.create(user=user, product=product, quantity=quantity)
        headers = self.get_success_headers(CartSerializer(created_cart).data)

        return Response(CartSerializer(created_cart).data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
