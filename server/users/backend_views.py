from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
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
    pagination_class = UsersNumberPagination
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['flags']


class UserApplicationsViewSet(viewsets.ModelViewSet):
    serializer_class = UserApplicationsSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<user_id> 参数，且设置basename
        :return:
        """
        return UserApplicationModel.objects.filter(user=self.kwargs['user_id'])




class UserLocationViewSet(viewsets.ModelViewSet):
    serializer_class = UserLocationSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<user_id> 参数，且设置basename
        :return:
        """
        return UserLocationModel.objects.filter(user=self.kwargs['user_id']).order_by('-created_at')[:1]


class UserDocsViewSet(viewsets.ModelViewSet):
    pagination_class = UsersNumberPagination
    serializer_class = UserDocSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<user_id> 参数，且设置basename
        :return:
        """
        return UserDocModel.objects.filter(user=self.kwargs['user_id'])


class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressesSerializer

    def get_queryset(self, *arg, **kwargs):
        """
        获得queryset，url中需含 P<user_id> 参数，且设置basename
        :return:
        """
        return UserAddressModel.objects.filter(user=self.kwargs['user_id'])


class UserBlackListViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserBlacklistSerializer
