from rest_framework import serializers

from cart.models import CartModel
from intentions.models import *


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'


class CarUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    """
    留言订单商品清单数据的序列化器
    """
    product = CartProductSerializer()
    quantity = serializers.IntegerField()
    user = CarUserSerializer()

    class Meta:
        model = CartModel
        fields = '__all__'
