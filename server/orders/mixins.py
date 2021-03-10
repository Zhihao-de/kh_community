from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from orders.models import OrderModel, OrderDetailModel, OrdersHistoryModel
from products.models import ProductModel


class OrderCreateModelMixin:
    """
    Create a order model instance.
    """

    def batch_create(self, request, *args, **kwargs):
        details = request.data.pop("details")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 在这里save
        self.perform_batch_create(serializer, details, args)
        headers = self.get_success_headers(serializer.data)
        return Response(list([detail for detail in details]),
                        status=status.HTTP_201_CREATED, headers=headers)

    def perform_batch_create(self, serializer, details, *args):
        with transaction.atomic():
            # save OrderModel
            res = serializer.save()
            # add details
            order = OrderModel.objects.get(id=res.id)
            # save order info to redis expire time(2h)

            for detail in details:
                if 'checked' in detail:
                    detail.pop('checked')
            total_weight = 0
            total_credit = 0
            durian_num = 0

            delivery_fee = 0
            # create order details
            for detail in details:
                product_id = detail.pop('product')["id"]
                quantity = int(detail['quantity'])
                product = ProductModel.objects.get(id=product_id)
                if (product.category in [3, 4, 5]):
                    durian_num += 1

                # 产品减库存？？？？ 是否在这里减
                # product.stock = product.stock - quantity
                # product.save()

                # 订单的毛重与积分与运费
                # cal = FreightCalculator(durian_num)
                # freight = cal.calculate()
                total_weight = total_weight + quantity * product.weight
                total_credit = total_credit + quantity * product.point

                # 增加订单的详情
                if order.user.flags == 2:
                    OrderDetailModel.objects.create(order=order, product=product,
                                                    price=product.purchase_price_register,
                                                    **detail)
                if order.user.flags == 5:
                    OrderDetailModel.objects.create(order=order, product=product,
                                                    price=product.purchase_price_corporate,
                                                    **detail)

            # 保存order的毛重
            order.tare = total_weight
            order.credit = total_credit
            order.save()
            # 保存order的历史
            OrdersHistoryModel.objects.create(user=order.user, list_amount=order.amount, tare=order.tare, is_paid=False,
                                              flags=0, created_at=order.created_at, updated_at=order.updated_at,
                                              order=order)

            # 创建之后要向订单MQ中发送 订单消息 设置TTL（自己是生产者）
            """
            print('发送消息开始')
            client = rabbit()
            msg = '消息发送至延时队列:' + order.serial_number
            client.publish_message('delay', msg, '', delay=1, TTL=60000)

            print('消息投递完成')
            """

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
