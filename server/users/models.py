from django.db import models


# Create your models here.


class UserModel(models.Model):
    """
    用户表（用户是指普通客户通过申请流程完成注册后的客户，即开皇社区/开皇妈妈）
    该表与django配套的auth_user表无关
    """
    wx_open_id = models.CharField(max_length=255, verbose_name='微信openid')
    wx_union_id = models.CharField(max_length=255, verbose_name='微信unionid')
    wx_name = models.CharField(max_length=255, verbose_name='微信名')
    wx_avatar_url = models.CharField(max_length=255, verbose_name="头像", default="")
    # mobile = models.CharField(max_length=16, blank=True, verbose_name='手机号')
    # 从 UserApplication 表同步的高频属性
    name = models.CharField(max_length=16, null=True, verbose_name='用户的真实姓名')
    gender = models.CharField(max_length=4, null=True, verbose_name='用户的真实性别')
    phone = models.CharField(max_length=16, null=True, verbose_name='用户的联系电话')
    email = models.CharField(max_length=255, null=True, verbose_name='用户的联系邮件')

    address_id = models.IntegerField(null=True, verbose_name='默认地址id')
    flags = models.SmallIntegerField(choices=[
        (0, '已申请'),
        (1, '待签协议'),
        (2, '已注册'),
        (3, '暂停'),
    ], verbose_name='用户状态')
    logined_at = models.DateTimeField(auto_now_add=True, verbose_name='最后登录时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kh_users'
        ordering = ["-id"]

    def user_save(self, nickname, avatar, sex, weixin_openid):
        if weixin_openid:
            print("找到了用户的openid")
            self.wx_name = nickname
            self.sex = sex
            self.avatar = avatar
            self.wx_open_id = weixin_openid
            self.save()
            print("该用户在user中不存在 目前还没有注册")
        return self

    def user_update(self, nickname, avatar, sex):
        if nickname:
            self.wx_name = nickname
            self.sex = sex
            self.avatar = avatar
            self.save()
            print("该用户在user中存在 已经是开皇用户")
        return self


class UserApplicationModel(models.Model):
    """
    用户申请表
    """
    user = models.ForeignKey(UserModel, related_name='user_applications',
                             on_delete=models.CASCADE, verbose_name='关联用户')
    name = models.CharField(max_length=16, verbose_name='用户的真实姓名')
    gender = models.CharField(max_length=4, verbose_name='用户的真实性别')
    phone = models.CharField(max_length=16, verbose_name='用户的联系电话')
    email = models.CharField(max_length=255, verbose_name='用户的联系邮件')
    ip = models.GenericIPAddressField(protocol="ipv4", db_index=True, verbose_name='注册地IP地址')
    idc_front_pic_url = models.CharField(max_length=255, verbose_name='证件照正面URL')
    idc_back_pic_url = models.CharField(max_length=255, verbose_name='证件照背面URL')
    reason_of_refusal = models.CharField(max_length=255, null=True, verbose_name='拒绝原因')
    flags = models.SmallIntegerField(choices=[
        (0, '待审批'),
        (1, '同意'),
        (2, '不同意'),
    ], verbose_name='申请状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')

    class Meta:
        db_table = 'kh_user_applications'
        ordering = ["-created_at"]


class UserLocationModel(models.Model):
    """
    用户地图位置
    """
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='关联用户')
    address = models.CharField(max_length=255, verbose_name='地图地址')
    lat = models.FloatField(max_length=255, verbose_name='地图纬度')
    lng = models.FloatField(max_length=255, verbose_name='地图经度')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')

    class Meta:
        db_table = 'kh_user_locations'


class UserAddressModel(models.Model):
    """
    用户（收件人）快递地址
    """
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='关联用户')
    contact_name = models.CharField(max_length=16, verbose_name='收件人姓名')
    contact_phone = models.CharField(max_length=16, verbose_name='收件人联系电话')
    country = models.CharField(max_length=255, default="中国", verbose_name='收件人国籍')
    province = models.CharField(max_length=255, verbose_name='收件人省份')
    city = models.CharField(max_length=255, verbose_name='收件人城市')
    district = models.CharField(max_length=255, verbose_name='收件人地区')
    address = models.CharField(max_length=255, verbose_name='收件人详细地址')
    postcode = models.CharField(max_length=255, verbose_name='收件人邮编')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    region = models.CharField(max_length=16, verbose_name='地区编号')

    class Meta:
        db_table = 'kh_user_addresses'


class UserDocModel(models.Model):
    """
    用户文档表
    """
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='关联用户')
    file_name = models.CharField(max_length=255, verbose_name='文件名称')
    file_type = models.CharField(max_length=255, verbose_name='文件类型')
    file_url = models.CharField(max_length=255, verbose_name='文件url')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'kh_user_docs'


class UserBlacklistModel(models.Model):
    """
    用户黑名单
    """
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='关联用户')
    reason = models.CharField(max_length=255, verbose_name='被暂停原因')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kh_user_blacklist'


class UserAccountModel(models.Model):
    """
    用户账本
    """
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='关联用户')
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name='单位元')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flags = models.SmallIntegerField(choices=[
        (0, '支出'),
        (1, '收入'),
    ], verbose_name='账目类别')

    class Meta:
        db_table = 'kh_user_accounts'
