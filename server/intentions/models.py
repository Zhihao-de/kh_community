from django.db import models

from products.models import ProductModel
from users.models import UserModel


class IntentionsModel(models.Model):
    """
    留言订单表
    """
    # 订单信息
    serial_number = models.CharField(max_length=255, verbose_name='留言订单编号')
    quantity = models.SmallIntegerField(default=0, verbose_name='商品数量')
    weight = models.DecimalField(max_digits=14, decimal_places=2, default=0.000)
    flags = models.SmallIntegerField(choices=[
        (0, '待分配'),
        (1, '已分配'),
        (2, '已完成'),
        (3, '已取消'),
        (4, '无法联系'),
    ], verbose_name='订单状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 客户信息
    # 客户微信信息
    wx_open_id = models.CharField(max_length=255, verbose_name='微信openid')
    wx_union_id = models.CharField(max_length=255, verbose_name='微信unionid')
    wx_name = models.CharField(max_length=255, verbose_name='微信名')
    wx_avatar_url = models.CharField(max_length=255, null=True, verbose_name='微信头像URL')
    # wx_mobile = models.CharField(max_length=11, null=True, verbose_name='手机号')
    # 客户联系信息
    name = models.CharField(max_length=16, verbose_name='客户姓名')
    phone = models.CharField(max_length=16, verbose_name='客户联系电话')
    country = models.CharField(max_length=255, default='中国', verbose_name='客户国籍')
    province = models.CharField(max_length=255, verbose_name='客户所在省份')
    city = models.CharField(max_length=255, verbose_name='客户所在城市')
    address = models.CharField(max_length=255, verbose_name='客户详细地址')
    postcode = models.CharField(max_length=255, verbose_name='客户地址的邮政编码')
    message = models.TextField(blank=True, verbose_name='客户留言')

    # 关联信息
    users = models.ManyToManyField(UserModel, through='IntentionAssignmentsModel', verbose_name='分配的用户')
    products = models.ManyToManyField(ProductModel, through='IntentionDetailsModel', verbose_name='商品列表')

    class Meta:
        db_table = 'kh_intentions'
        ordering = ['-id']


class IntentionDetailsModel(models.Model):
    """
    留言订单的商品明细表
    """
    intention = models.ForeignKey(IntentionsModel, on_delete=models.CASCADE, verbose_name='关联的留言订单')
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING, verbose_name='关联的产品')
    quantity = models.IntegerField(default=1, verbose_name='订购数量')
    retail_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name='交易单价元')

    class Meta:
        db_table = 'kh_intention_details'


class IntentionAssignmentsModel(models.Model):
    """
    留言订单的用户分配表
    """
    intention = models.ForeignKey(IntentionsModel, on_delete=models.CASCADE, verbose_name='关联的留言订单')
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, verbose_name='关联的用户')
    remark = models.CharField(max_length=255, blank=True, verbose_name='备注')
    flags = models.SmallIntegerField(choices=[
        (0, '正常'),
        (1, '超时'),
        (2, '删除'),
        (3, '完成'),
    ], default=0, verbose_name='分配状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='分配时间')

    class Meta:
        db_table = 'kh_intention_assignments'


# 每当留言订单发生变更这里就要添加一条记录
class IntentionsHistoryModel(models.Model):
    """
    留言订单历史
    """
    serial_number = models.CharField(max_length=255, verbose_name='留言订单编号')
    quantity = models.SmallIntegerField(default=0, verbose_name='商品数量')
    weight = models.DecimalField(max_digits=14, decimal_places=2, default=0.000)
    flags = models.SmallIntegerField(choices=[
        (0, '待分配'),
        (1, '已分配'),
        (2, '已完成'),
        (3, '已取消'),
        (4, '无法联系'),
    ], verbose_name='订单状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 客户信息
    # 客户微信信息
    wx_open_id = models.CharField(max_length=255, verbose_name='微信openid')
    wx_union_id = models.CharField(max_length=255, verbose_name='微信unionid')
    wx_name = models.CharField(max_length=255, verbose_name='微信名')
    wx_avatar_url = models.CharField(max_length=255, null=True, verbose_name='微信头像URL')
    # wx_mobile = models.CharField(max_length=11, null=True, verbose_name='手机号')
    # 客户联系信息
    name = models.CharField(max_length=16, verbose_name='客户姓名')
    phone = models.CharField(max_length=16, verbose_name='客户联系电话')
    country = models.CharField(max_length=255, default='中国', verbose_name='客户国籍')
    province = models.CharField(max_length=255, verbose_name='客户所在省份')
    city = models.CharField(max_length=255, verbose_name='客户所在城市')
    address = models.CharField(max_length=255, verbose_name='客户详细地址')
    postcode = models.CharField(max_length=255, verbose_name='客户地址的邮政编码')
    message = models.TextField(blank=True, verbose_name='客户留言')

    intention = models.ForeignKey(IntentionsModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'kh_intentions_history'


class IntentionDetailsHistoryModel(models.Model):
    """
    留言订单历史
    """
    intention = models.ForeignKey(IntentionsHistoryModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=14, decimal_places=2, default=1.00)
    retail_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'kh_intention_details_history'
