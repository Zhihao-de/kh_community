from django.db import models
from django.utils import timezone

from products.models import ProductModel
from users.models import UserModel


# Create your models here.

class OrderModel(models.Model):
    """
    产品订单表
    """
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, verbose_name='关联用户')
    #
    serial_number = models.CharField(max_length=255, verbose_name='订单编号')
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name='订单金额')
    tare = models.DecimalField(max_digits=14, decimal_places=2, default=0.000, verbose_name='毛重')
    quantity = models.SmallIntegerField(default=0, verbose_name='商品数量')
    # 物流信息
    name = models.CharField(max_length=16, verbose_name='收货人姓名')
    phone = models.CharField(max_length=16, verbose_name='收货人联系电话')
    country = models.CharField(max_length=255, default='中国', verbose_name='收货人国籍')
    province = models.CharField(max_length=255, verbose_name='收货人所在省份')
    city = models.CharField(max_length=255, verbose_name='收货人所在城市')
    address = models.CharField(max_length=255, verbose_name='收货人详细地址')
    postcode = models.CharField(max_length=255, verbose_name='收货人地址的邮政编码')
    message = models.TextField(blank=True, verbose_name='收货人备注')
    # 退款信息 退款订单号一般同原订单号
    refund_number = models.CharField(blank=True, max_length=64, verbose_name='退款订单')
    refund_reason = models.TextField(blank=True, verbose_name='收货人备注')
    #
    flags = models.SmallIntegerField(choices=[
        (0, '未付款'),
        (1, '已付款'),
        (2, '配送中'),
        (3, '已签收'),
        (4, '已取消'),
        (5, '退款中'),
        (6, '已退款'),

    ], default=0, verbose_name='订单状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        db_table = 'kh_orders'
        ordering = ['-id']


class OrderTransactionModel(models.Model):
    """
    订单交易记录表
    """
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, verbose_name='关联订单')
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name='支付金额')
    payment_method = models.SmallIntegerField(choices=[
        (0, '支付宝'),
        (1, '微信支付'),
        (2, '银行卡'),
        (3, '其他'),
    ], default=1, verbose_name='支付方式')
    transaction_id = models.CharField(max_length=64, default="00000000000000000000000000000000", verbose_name='交易ID')
    paid_at = models.DateTimeField(null=True, verbose_name='付款时间')
    refund = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name='投款金额')
    refunded_at = models.DateTimeField(null=True, verbose_name='退款时间')
    status = models.CharField(max_length=255, null=True, verbose_name='交易状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kh_order_transactions'


class OrderRouteModel(models.Model):
    """
    订单物流记录表
    """
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, verbose_name='关联订单')
    express = models.CharField(max_length=32, verbose_name='物流服务名称')
    receipt_no = models.CharField(max_length=255, unique=True, verbose_name='物流单号')
    address = models.CharField(max_length=512, verbose_name='发货地址')
    quantity = models.IntegerField(default=0, verbose_name='数量')
    weight = models.DecimalField(max_digits=14, decimal_places=3, default=0.000, verbose_name='总重千克')
    cost = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name='运费')
    remark = models.TextField(blank=True, verbose_name='备注')
    routes = models.TextField(blank=True, verbose_name='物流过程')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        db_table = 'kh_order_routes'


class OrderDetailModel(models.Model):
    """
    产品订单明细
    """
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, verbose_name='关联订单')
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING, verbose_name='关联产品')
    # productUnit = models.ForeignKey(ProductUnitModel, on_delete=models.DO_NOTHING, verbose_name='关联产品SKU')
    purchase_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name='交易单价元')
    quantity = models.IntegerField(default=0, verbose_name='商品数量')

    class Meta:
        db_table = 'kh_order_details'


class OrdersHistoryModel(models.Model):
    """
    产品订单历史
    """
    PAY_CHOICES = [
        (0, '支付宝'),
        (1, '微信支付'),
        (2, '银行卡'),
        (3, '其他'),
    ]
    FLAG_CHOICES = [
        (0, '未付款'),
        (1, '已付款'),
        (2, '配送中'),
        (3, '已签收'),
        (4, '已取消'),
        (5, '退款中'),
        (6, '已退款'),
    ]
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    serial_number = models.CharField(max_length=255, verbose_name='订单编号')
    list_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.000)
    tare = models.DecimalField(max_digits=14, decimal_places=2, default=0.000)
    payment_method = models.SmallIntegerField(choices=PAY_CHOICES, default=1)
    is_paid = models.BooleanField(blank=True, default=True)
    transaction_id = models.CharField(max_length=64, default="00000000000000000000000000000000")
    paid_at = models.DateTimeField(default=timezone.now)
    refund = models.DecimalField(max_digits=14, decimal_places=2, default=0.000)
    flags = models.SmallIntegerField(choices=FLAG_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, verbose_name='关联订单')

    class Meta:
        db_table = 'kh_orders_history'


class OrderDetailsHistoryModel(models.Model):
    """
    产品订单明细历史
    """
    order = models.ForeignKey(OrdersHistoryModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING)
    #    productUnit = models.ForeignKey(ProductUnitModel, on_delete=models.DO_NOTHING, verbose_name='关联产品SKU')
    quantity = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=14, decimal_places=3, default=0.000)

    class Meta:
        db_table = 'kh_order_details_history'
