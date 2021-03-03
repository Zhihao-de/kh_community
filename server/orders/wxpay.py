import datetime
import decimal
import hashlib
import json
import socket
import time
import xml.etree.ElementTree as elementTree

import requests
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from orders.models import OrderModel, OrderDetailModel, OrdersHistoryModel
from orders.models import OrderTransactionModel
from products.models import ProductModel
from users import response_code


def get_openid_by_code(code):
    """
    get wechat open id
    """
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'
    get_url = url.format(settings.WEIXIN_APPID, settings.WEIXIN_SECRET, code)
    r = requests.get(get_url)
    return r.json()


def paysign(body, nonce_str, openid, out_trade_no, spbill_create_ip, total_fee):
    """
    微信支付信息：
    包含appid,商户号，随机字符串，微信openid
    """

    ret = {
        'appid': settings.WEIXIN_APPID,
        'body': body,
        'mch_id': settings.MCH_ID,
        'nonce_str': nonce_str,
        'notify_url': settings.NOTIFY_URL,
        'openid': openid,
        'out_trade_no': out_trade_no,
        'spbill_create_ip': spbill_create_ip,
        'total_fee': total_fee,
        'trade_type': 'JSAPI',
    }

    # 处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
    stringA = '&'.join(["{0}={1}".format(k, ret.get(k)) for k in sorted(ret)])
    stringSignTemp = '{0}&key={1}'.format(stringA, settings.MCH_KEY)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()


def mini_paysign(nonce_str, prepay_id, timeStamp):
    """
    微信迷你支付信息：
    包含appid,商户号，随机字符串，微信openid，加密类型，事件时间戳
    """

    ret = {
        'appId': settings.WEIXIN_APPID,
        'nonceStr': nonce_str,
        'package': 'prepay_id=' + prepay_id,
        'signType': 'MD5',
        'timeStamp': timeStamp,
    }

    # 处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
    stringA = '&'.join(["{0}={1}".format(k, ret.get(k)) for k in sorted(ret)])
    stringSignTemp = '{0}&key={1}'.format(stringA, settings.MCH_KEY)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()


def get_body_data(body, nonce_str, openid, out_trade_no, spbill_create_ip, total_fee):
    """
    get post data to request of payment
    """
    total_fee = str(total_fee)
    # 生成签名
    sign = paysign(body, nonce_str, openid, out_trade_no, spbill_create_ip, total_fee)

    body_data = '<xml>'
    body_data += '<appid>' + settings.WEIXIN_APPID + '</appid>'  # 小程序ID
    body_data += '<body>' + body + '</body>'  # 商品描述
    body_data += '<mch_id>' + settings.MCH_ID + '</mch_id>'  # 商户号
    body_data += '<nonce_str>' + nonce_str + '</nonce_str>'  # 随机字符串
    body_data += '<notify_url>' + settings.NOTIFY_URL + '</notify_url>'  # 通知地址
    body_data += '<openid>' + openid + '</openid>'  # 用户标识
    body_data += '<out_trade_no>' + out_trade_no + '</out_trade_no>'  # 商户订单号
    body_data += '<spbill_create_ip>' + spbill_create_ip + '</spbill_create_ip>'  # 终端IP
    body_data += '<total_fee>' + total_fee + '</total_fee>'  # 标价金额
    body_data += '<trade_type>JSAPI</trade_type>'  # 交易类型
    body_data += '<sign>' + sign + '</sign>'  # 签名
    body_data += '</xml>'

    return body_data


def get_host_ip():
    """
    check local ip
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def getNoceStr():
    """
    random string to get pay sign
    """

    import random
    data = "1234567890qwertyuiopasdfghjkRTUERlzxcvbnmASDFGHJKLPOIUYT"
    nonce_str = ''.join(random.sample(data, 30))
    return nonce_str


def xml_to_dict(xml_data):
    """
    xml to dict
    :param xml_data:
    :return:
    """
    xml_dict = {}
    root = elementTree.fromstring(xml_data)
    for child in root:
        xml_dict[child.tag] = child.text
    return xml_dict


def dict_to_xml(dict_data):
    """
    dict to xml
    :param dict_data:
    :return:
    """
    xml = ["<xml>"]
    for k, v in dict_data.iteritems():
        xml.append("<{0}>{1}</{0}>".format(k, v))
    xml.append("</xml>")
    return "".join(xml)


def time_shift(time):
    """
    shift string "end_time" to datetime
    """
    year = time[0:4]
    month = time[4:6]
    day = time[6:8]
    hour = time[8:10]
    minute = time[10:12]
    sec = time[12:14]
    formed_time = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + sec
    time_format = '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.strptime(formed_time, time_format)


@csrf_exempt
def payOrder(request):
    """
    send request to wechat pay and operate orders
    """
    json_data = json.loads(request.body)
    user_code = json_data['code']
    serial = json_data['serial']
    orderObj = OrderModel.objects.get(serial_number=serial)
    if orderObj.flags != 0:
        res = {
            'errno': response_code.SYS_ERR,
            'statusCode': 200,
            'errMsg': '已经支付过了'
        }
        return JsonResponse(res)
    json_data_wx = get_openid_by_code(user_code)
    if 'errcode' in json_data_wx:
        res = {
            'errno': response_code.AUTH_ERROR,
            'statusCode': 200,
            'errMsg': '出错了:' + json_data_wx['errmsg']
        }
        return JsonResponse(res)
    openid = json_data_wx['openid']
    body = "开皇社区"
    nonce_str = getNoceStr()
    out_trade_no = orderObj.serial_number
    spbill_create_ip = get_host_ip()
    # total_fee = int(orderObj.amount * 100)
    total_fee = 1
    print('设置为支付1分钱')
    body_data = get_body_data(body, nonce_str, openid, out_trade_no, spbill_create_ip, total_fee)
    # 发送请求
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    response = requests.post(url, body_data.encode("utf-8"), headers={'Content-Type': 'application/xml'})
    content = xml_to_dict(response.content)
    print("这里是返回信息")
    print(content)
    if content['return_code'] == 'SUCCESS':

        with transaction.atomic():
            prepay_id = content.get('prepay_id')
            nonce_str = content.get('nonce_str')
            timeStamp = str(int(time.time()))
            # 小程序调起支付数据签名
            paySign = mini_paysign(nonce_str, prepay_id, timeStamp)
            res = {
                'errno': response_code.IS_SUCCESS,
                'statusCode': 200,
                'errMsg': '获取成功',
                'data': {
                    'timeStamp': timeStamp,
                    'nonceStr': nonce_str,
                    'prepay_id': prepay_id,
                    'paySign': paySign
                }
            }

            return JsonResponse(res)
    else:
        res = {
            'errno': response_code.SYS_ERR,
            'statusCode': 200,
            'errMsg': '失败',
            'data': {

            }
        }
        return JsonResponse(res)


# 支付回调
@csrf_exempt
def wxpayback(request):
    """
    wechat pay call back to get transaction info and deal with product stock and order flags
    """
    msg = request.body.decode('utf-8')
    dictmsg = xml_to_dict(msg)
    print(dictmsg)
    return_code = dictmsg['return_code']
    if return_code == 'SUCCESS':
        with transaction.atomic():
            out_trade_no = dictmsg['out_trade_no']
            # 更改订单状态
            order = OrderModel.objects.get(serial_number=out_trade_no)
            order.flags = 1
            order.save()
            print(order.serial_number + "的信息已经更改为已经支付")
            # 增加transaction 信息
            trans = OrderTransactionModel()
            trans.order = order
            amount = decimal.Decimal(dictmsg['total_fee'])
            amount_decimal = amount / 100
            trans.amount = amount_decimal

            trans.transaction_id = dictmsg['transaction_id']
            time_format = '%Y-%m-%d %H:%M:%S'
            now_time = datetime.datetime.now().strftime(time_format)
            trans.created_at = now_time
            trans.paid_at = time_shift(dictmsg['time_end'])
            trans.status = 0
            trans.save()
            print('增加支付订单信息')
            # 修改订单历史
            OrdersHistoryModel.objects.create(user=order.user,
                                              list_amount=order.amount,
                                              tare=order.tare,
                                              payment_method=1,
                                              is_paid=True,
                                              transaction_id=trans.transaction_id,
                                              paid_at=trans.paid_at,
                                              refund=0,
                                              flags=1,
                                              created_at=order.created_at,
                                              updated_at=trans.paid_at,
                                              order=order)

            # 查数量改库存
            details = OrderDetailModel.objects.filter(order_id=order.id)

            # 这里需要发一条消息

            for product_info in details:
                pro = ProductModel.objects.get(id=product_info.product.id)
                pro.stock = product_info.product.stock - product_info.quantity
                print(product_info.product.name + "的余量为:" + str(pro.stock))
                pro.save()

            return HttpResponse("""<xml><return_code><![CDATA[SUCCESS]]></return_code>
                        <return_msg><![CDATA[OK]]></return_msg></xml>""")
    else:
        return HttpResponse("""<xml><return_code><![CDATA[FAIL]]></return_code>
                <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""")


##################################################################################
def mini_payrefunsign(nonce_str, out_refund_no, out_trade_no, refund_fee):
    ret = {
        'appid': settings.WEIXIN_APPID,
        'mch_id': settings.MCH_ID,
        'nonce_str': nonce_str,
        'out_refund_no': out_refund_no,
        'out_trade_no': out_trade_no,
        'refund_fee': refund_fee,
        'total_fee': refund_fee
    }

    # 处理函数，对参数按照key=value的格式，并按照参数名ASCII字典序排序
    stringA = '&'.join(["{0}={1}".format(k, ret.get(k)) for k in sorted(ret)])
    stringSignTemp = '{0}&key={1}'.format(stringA, settings.MCH_KEY)
    sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
    return sign.upper()


def refundBody(nonce_str, out_refund_no, out_trade_no, refund_fee):
    """
    refund post data in form of XML
    """
    refund_fee = str(refund_fee)
    sign = mini_payrefunsign(nonce_str, out_refund_no, out_trade_no, refund_fee)
    body_data = '<xml>'
    body_data += '<appid>' + settings.WEIXIN_APPID + '</appid>'  # 小程序ID
    body_data += '<mch_id>' + settings.MCH_ID + '</mch_id>'  # 商户号
    body_data += '<nonce_str>' + nonce_str + '</nonce_str>'  # 随机字符串
    body_data += '<out_refund_no>' + out_refund_no + '</out_refund_no>'  # 退款单号
    body_data += '<notify_url>' + settings.NOTIFY_URL_REFUND + '</notify_url>'  # 通知地址
    body_data += '<out_trade_no>' + out_trade_no + '</out_trade_no>'  # 商户订单号
    body_data += '<refund_fee>' + refund_fee + '</refund_fee>'  # 退款金额
    body_data += '<total_fee>' + refund_fee + '</total_fee>'  # 标价金额
    body_data += '<sign>' + sign + '</sign>'  # 标价金额
    body_data += '</xml>'

    return body_data


@csrf_exempt
def wxpayrefund(request):
    """
    wechat refund request
    """
    json_data = json.loads(request.body)
    serial = json_data['serial']
    with transaction:
        # 一体退款 将订单的退款订单号就是订单序列号(也可以自定义)
        refund_order = OrderModel.objects.get(serial_number=serial)
        # refund_order.refund_number = refund_order.serial_number
        # refund_order.save()
        # 组织请求需要的发送的xml信息
        out_refund_no = refund_order.serial_number
        out_trade_no = refund_order.serial_number
        refund_fee = int(refund_order.amount * 100)
        nonce_str = getNoceStr()
        body_data = refundBody(nonce_str, out_refund_no, out_trade_no, refund_fee)
        url = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
        # 请求
        response = requests.post(url, cert=(settings.CERT_PATH, settings.KEY_PATH), data=body_data.encode("utf-8"))

        # 增加退款的transaction信息
        refund_trans = OrderTransactionModel()
        # 将库存数量返回
        details = OrderDetailModel.objects.filter(order_id=refund_order.id)
        for product_info in details:
            pro = ProductModel.objects.get(id=product_info.product.id)
            pro.stock = product_info.product.stock + product_info.quantity
            print(product_info.product.name + "的余量为:" + str(pro.stock) + ":" + "增加了" + str(product_info.quantity))
            pro.save()

        # 将订单的状态转为'已退款'
        refund_order.refund_number = refund_order.serial_number
        refund_order.flags = 6
        print(response.content)

        return 23423423


@csrf_exempt
def refundback(request):
    """
    wechat refund call back
    """
    msg = request.body.decode('utf-8')
    if (msg):
        dictmsg = xml_to_dict(msg)
        print(dictmsg)
        return HttpResponse("""<xml><return_code><![CDATA[SUCCESS]]></return_code>
                            <return_msg><![CDATA[OK]]></return_msg></xml>""")
    else:
        return HttpResponse("""<xml><return_code><![CDATA[FAIL]]></return_code>
                    <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""")
