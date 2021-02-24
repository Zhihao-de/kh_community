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
            for detail in details:
                product_id = detail.pop('product')["id"]
                quantity = int(detail['quantity'])
                product = ProductModel.objects.get(id=product_id)
                total_weight = total_weight + quantity * product.weight
                # 创建订单
                OrderDetailModel.objects.create(order=order, product=product, purchase_price=product.purchase_price,
                                                **detail)
            # 保存order的毛重
            order.tare = total_weight
            order.save()
            # 保存order的历史
            OrdersHistoryModel.objects.create(user=order.user, list_amount=order.amount, tare=order.tare, is_paid=False,
                                              flags=0, created_at=order.created_at, updated_at=order.updated_at,
                                              order=order)
            # 将order数据保存至cache 等待过期消息
            con = Daemon()
            con.set_value(order.serial_number, "", 10)

            print(con.get_value(order.serial_number))

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
