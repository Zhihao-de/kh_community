import datetime

import pytz
from django.db import transaction
from rest_framework import serializers

from intentions.models import *
from until.listen import Daemon


class IntentionsReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = IntentionsModel
        fields = '__all__'


class IntentionSerializer(serializers.ModelSerializer):
    """
    留言订单数据的序列化器
    """
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    def create(self, validated_data):
        print("nasnsancasjnckjasncjasncjasncjknascjnaskjcnajkscnkjascnkasnckasncjkasnckjanscnasjcnaskc")
        return IntentionsModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.flags = validated_data["flags"]
            instance.save()
            IntentionsHistoryModel.objects.create(serial_number=instance.serial_number,
                                                  quantity=instance.quantity,
                                                  weight=instance.weight, flags=instance.flags,
                                                  created_at=instance.created_at, updated_at=instance.updated_at,
                                                  wx_open_id=instance.wx_open_id,
                                                  wx_union_id=instance.wx_union_id,
                                                  wx_name=instance.wx_name, wx_avatar_url=instance.wx_avatar_url,
                                                  name=instance.name, phone=instance.phone,
                                                  country=instance.country,
                                                  province=instance.province, city=instance.city,
                                                  address=instance.address, postcode=instance.postcode,
                                                  message=instance.postcode, intention=instance)

        return instance

    class Meta:
        model = IntentionsModel
        exclude = ['users', 'products']


class IntentionProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'weight', 'unit']


class IntentionDetailsSerializer(serializers.ModelSerializer):
    """
    留言订单商品清单数据的序列化器
    """
    intention = IntentionSerializer()
    product = IntentionProductsSerializer()
    total_price = serializers.SerializerMethodField()

    @staticmethod
    def get_total_price(obj):
        """
        获得总价
        :param obj: OrderDetail对象
        :return:
        """
        return '%.02f' % (obj.retail_price * obj.quantity)

    class Meta:
        model = IntentionDetailsModel
        fields = ['id', 'product', 'intention', 'retail_price', 'quantity', 'total_price']


class IntentionDetailsFrontSerializer(serializers.ModelSerializer):
    """
    留言订单商品清单数据的序列化器
    """
    total_price = serializers.SerializerMethodField()

    @staticmethod
    def get_total_price(obj):
        """
        获得总价
        :param obj: OrderDetail对象
        :return:
        """
        return '%.02f' % (obj.retail_price * obj.quantity)

    class Meta:
        model = IntentionDetailsModel
        fields = ['id', 'product', 'intention', 'retail_price', 'quantity', 'total_price']


class IntentionUserSerializer(serializers.ModelSerializer):
    """
    留言订单分配用户的序列化器
    与UsersSerializer区别在于，本序列化器仅要求id为必须项，并简化了非必要字段
    """
    wx_name = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = UserModel
        fields = ['id', 'wx_name', 'wx_avatar_url', 'name', 'gender', 'phone', 'email']


class IntentionAssignmentSerializer(serializers.ModelSerializer):
    """
    留言订单分配数据的序列化器
    """
    # user = IntentionUserSerializer()
    # intention = IntentionSerializer()

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    expired_days = serializers.SerializerMethodField()

    @staticmethod
    def get_expired_days(instance):
        now = datetime.datetime.now()
        now = now.replace(tzinfo=pytz.timezone('UTC'))
        return (now - instance.created_at).days

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['expired_days'] > 0:
            data['flags'] = 1
        return data

    def create(self, validate):
        """
        创建单个的分配记录
        :return:
        """
        with transaction.atomic():
            user_id = self.initial_data['user']
            print(user_id)
            user = UserModel.objects.get(id=user_id)
            intention_id = self.initial_data['intention']
            intention = IntentionsModel.objects.get(id=intention_id)
            # 首先获得作为外键的UserModel对象，然后连同其他字段一同创建
            res = IntentionAssignmentsModel.objects.create(user=user, intention=intention, remark='委任分派', flags=0)
            # 使用redis 保存assignment的数据 保证过期时间
            con = Daemon()
            con.set_value(intention.serial_number, "x", 10)

            # 最后修改intention的状态
            IntentionsModel.objects.filter(id=intention_id).update(flags=1)

            # 创建历史记录
            IntentionsHistoryModel.objects.create(serial_number=intention.serial_number,
                                                  quantity=intention.quantity,
                                                  weight=intention.weight, flags=intention.flags,
                                                  created_at=intention.created_at, updated_at=intention.updated_at,
                                                  wx_open_id=intention.wx_open_id,
                                                  wx_union_id=intention.wx_union_id,
                                                  wx_name=intention.wx_name, wx_avatar_url=intention.wx_avatar_url,
                                                  name=intention.name, phone=intention.phone,
                                                  country=intention.country,
                                                  province=intention.province, city=intention.city,
                                                  address=intention.address, postcode=intention.postcode,
                                                  message=intention.postcode, intention=intention)
            return res

    def update(self, instance, validated_data):
        """
        finish assignment and intention
        """
        with transaction.atomic():
            print("safsasfbaskjfjasnfsajnfnasjfnajksnfasjfnasjk")
            print(self.initial_data['flags'])
            assignment_id = self.initial_data['id']
            assignment = IntentionAssignmentsModel.objects.get(id=assignment_id)
            assignment.flags = self.initial_data['flags']
            assignment.save()
            intention_id = self.initial_data['intention']
            intention = IntentionsModel.objects.get(id=intention_id)
            intention.flags = 2
            intention.save()
            IntentionsHistoryModel.objects.create(serial_number=intention.serial_number,
                                                  quantity=intention.quantity,
                                                  weight=intention.weight, flags=intention.flags,
                                                  created_at=intention.created_at, updated_at=intention.updated_at,
                                                  wx_open_id=intention.wx_open_id,
                                                  wx_union_id=intention.wx_union_id,
                                                  wx_name=intention.wx_name, wx_avatar_url=intention.wx_avatar_url,
                                                  name=intention.name, phone=intention.phone,
                                                  country=intention.country,
                                                  province=intention.province, city=intention.city,
                                                  address=intention.address, postcode=intention.postcode,
                                                  message=intention.postcode, intention=intention)
            return assignment

    class Meta:
        model = IntentionAssignmentsModel
        fields = '__all__'
        depth = 1


# 留言订单历史序列化器
class IntentionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IntentionsHistoryModel
        fields = '__all__'

#
