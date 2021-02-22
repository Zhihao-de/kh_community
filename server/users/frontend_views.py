from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from users.serializers import *


class UsersNumberPagination(PageNumberPagination):
    page_size = 4
    max_page_size = 50
    page_size_query_param = 'page_size'
    page_query_param = 'page'


class UsersViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UsersSerializer


class UserApplicationsViewSet(viewsets.ModelViewSet):
    serializer_class = UserApplicationsSerializer

    def get_queryset(self, *arg, **kwargs):
        """
        获得queryset，url中需含 P<user_id> 参数，且设置basename
        :return:
        """
        return UserApplicationModel.objects.filter(user=self.kwargs['user_id'])


class UserLocationViewSet(viewsets.ModelViewSet):
    queryset = UserLocationModel.objects.all()
    serializer_class = UserLocationSerializer


class UserDocsViewSet(viewsets.ModelViewSet):
    queryset = UserDocModel.objects.all()
    serializer_class = UserDocSerializer


class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddressModel.objects.all()
    serializer_class = UserAddressesSerializer


class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccountModel.objects.all()
    serializer_class = UserAccountSerializer


class UserBlackListViewSet(viewsets.ModelViewSet):
    serializer_class = UserBlacklistSerializer

    def get_queryset(self, *arg, **kwargs):
        """
        获得queryset，url中需含 P<user_id> 参数，且设置basename
        :return:
        """
        return UserBlacklistModel.objects.filter(user=self.kwargs['user_id'])
