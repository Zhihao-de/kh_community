from rest_framework import serializers

from orders.models import *


class OrderUserSerializer(serializers.ModelSerializer):
    """
    商品订单分配用户的序列化器
    """

    class Meta:
        model = UserModel
        fields = ['id', 'wx_name', 'wx_avatar_url', 'name', 'gender', 'phone', 'email']


class OrdersSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    # 确保被每一次update都有history更新
    class Meta:
        model = OrderModel
        fields = '__all__'


"""
 def update(self, instance, validated_data):
     with transaction.atomic():
         trans = OrderTransactionModel.objects.get(order=instance)
         if trans:
             transaction_id = trans.transaction_id
             paid = True
         else:
             transaction_id = 'none'
             paid = False

         instance.flags = validated_data["flags"]
         instance.save()
         OrdersHistoryModel.objects.create(user=instance.user,
                                           list_amount=instance.amount,
                                           tare=instance.tare,
                                           payment_method=trans.payment_method,
                                           is_paid=paid,
                                           transaction_id=transaction_id,
                                           paid_at=trans.paid_at,
                                           refund=trans.refund,
                                           flags=instance.flags,
                                           created_at=instance.created_at,
                                           updated_at=instance.updated_at,
                                           serial_number=instance.serial_number,
                                           order=instance)

     return instance
     """


# 前端的序列化器
class OrderFrontSerializer(serializers.ModelSerializer):
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = OrderModel
        fields = '__all__'


class OrderTransactionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = OrderTransactionModel
        fields = '__all__'


class OrderProductsSerializer(serializers.ModelSerializer):
    """
    商品订单中商品明细数据的序列化器
    """

    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'weight', 'unit', 'pic_url']


class OrderDetailsSerializer(serializers.ModelSerializer):
    """
    商品订单详情数据的序列化器
    """
    product = OrderProductsSerializer(required=False, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        """
        获得总价
        :param obj: OrderDetail对象
        :return:
        """
        return '%.02f' % (obj.purchase_price * obj.quantity)

    class Meta:
        model = OrderDetailModel
        fields = ['id', 'product', 'purchase_price', 'quantity', 'total_price']


class OrderDetailsFrontSerializer(serializers.ModelSerializer):
    """
    商品订单详情数据的序列化器
    """
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        """
        获得总价
        :param obj: OrderDetail对象
        :return:
        """
        return '%.02f' % (obj.purchase_price * obj.quantity)

    class Meta:
        model = OrderDetailModel
        fields = ['id', 'product', 'purchase_price', 'quantity', 'total_price']


class OrderRoutesSerializer(serializers.ModelSerializer):
    """
    商品订单物流数据的序列化器
    """

    class Meta:
        model = OrderRouteModel
        fields = '__all__'


class OrderHistorySerializer(serializers.ModelSerializer):
    """
     商品订单历史数据的序列化器
     """

    class Meta:
        model = OrdersHistoryModel
        fields = '__all__'
        depth = 1
