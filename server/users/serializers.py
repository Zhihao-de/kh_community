from rest_framework import serializers

from users.models import *


class UsersReadonlySerializer(serializers.ModelSerializer):
    wx_name = serializers.CharField()
    # mobile = serializers.CharField()
    logined_at = serializers.DateTimeField

    class Meta:
        model = UserModel
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    """
    用户数据的序列化器
    """
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    logined_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = UserModel
        fields = '__all__'


class UserApplicationsSerializer(serializers.ModelSerializer):
    """
    用户申请数据的序列化器
    """
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = UserApplicationModel
        fields = '__all__'
        ordering = ['-created_at']

    def create(self, validate):
        """
        在用户更新最新的application的时候自动获取用户的部分信息
        """
        print("这里使用户的申请信息")
        validate.pop('user')
        user_id = self.initial_data['user']
        print(user_id)
        user = UserModel.objects.get(id=user_id)
        # 根据申请表更新用户的信息
        user.phone = validate['phone']
        user.name = validate['name']
        user.gender = validate['gender']
        user.email = validate['email']
        user.save()
        # 创建新的application
        res = UserApplicationModel.objects.create(user=user, **validate)

        return res


class UserLocationSerializer(serializers.ModelSerializer):
    """
    用户地图位置数据的序列化器
    """
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = UserLocationModel
        fields = '__all__'


class UserAccountSerializer(serializers.ModelSerializer):
    """
    用户地图位置数据的序列化器
    """
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = UserAccountModel
        fields = '__all__'


class UserDocSerializer(serializers.ModelSerializer):
    """
    用户地图位置数据的序列化器
    """
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = UserDocModel
        fields = '__all__'


class UserAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddressModel
        fields = '__all__'


class UserBlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBlacklistModel
        fields = '__all__'
