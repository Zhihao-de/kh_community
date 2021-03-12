import datetime
import decimal
import json
import uuid

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from orders.models import OrderModel, OrderTransactionModel, OrdersHistoryModel, OrderDetailModel
from products.models import ProductModel
from users import response_code
from users.models import UserModel


@csrf_exempt
def payOrder(request):
    json_data = json.loads(request.body)
    # 订单信息
    serial = json_data['serial']
    orderObj = OrderModel.objects.get(serial_number=serial)
    # 用户信息
    open_id = json_data['open_id']
    userObj = UserModel.objects.get(wx_open_id=open_id)
    # 订单需要支付的金额
    amount = decimal.Decimal(json_data['amount'])
    actual_payment = decimal.Decimal(json_data['actual_payment'])

    if orderObj.flags != 0:
        res = {
            'errno': response_code.SYS_ERR,
            'statusCode': 200,
            'errMsg': '已经支付过了'
        }
        return JsonResponse(res)
    if orderObj.flags == 0:
        with transaction.atomic():
            # 减少用户的余额
            userObj.balance = userObj.balance - actual_payment

            # 增加支付所产生的积分
            userObj.credit = userObj.credit + orderObj.credit
            userObj.save()

            # 更改订单状态
            orderObj.flags = 1
            orderObj.save()
            # 增加支付信息
            trans = OrderTransactionModel()
            trans.order = orderObj
            trans.amount = actual_payment

            trans.payment_method = 2
            uuid_value = uuid.uuid1()
            uuid_str = uuid_value.hex
            trans.transaction_id = uuid_str
            time_format = '%Y-%m-%d %H:%M:%S'
            now_time = datetime.datetime.now().strftime(time_format)
            trans.created_at = now_time
            trans.paid_at = now_time
            trans.status = 0
            trans.save()
            # 增加订单历史
            OrdersHistoryModel.objects.create(
                user=userObj,
                list_amount=actual_payment,
                tare=orderObj.tare,
                payment_method=2,
                is_paid=True,
                transaction_id=trans.transaction_id,
                paid_at=trans.paid_at,
                refund=0,
                flags=1,
                created_at=orderObj.created_at,
                updated_at=trans.paid_at,
                order=orderObj
            )
            # 查数量改库存
            details = OrderDetailModel.objects.filter(order_id=orderObj.id)
            # 支付成功之后减库存
            for product_info in details:
                pro = ProductModel.objects.get(id=product_info.product.id)
                pro.stock = product_info.product.stock - product_info.quantity
                print(product_info.product.name + "的余量为:" + str(pro.stock))
                pro.save()

            res = {
                'errno': response_code.IS_SUCCESS,
                'statusCode': 200,
                'errMsg': '支付成功！',

            }
            return JsonResponse(res)
