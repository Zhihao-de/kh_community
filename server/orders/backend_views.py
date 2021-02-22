from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from orders.serizalizers import *


# Create your views here.

class OrdersNumberPagination(PageNumberPagination):
    page_size = 4
    max_page_size = 50
    page_size_query_param = 'page_size'
    page_query_param = 'page'


class OrdersViewReadonlySet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrdersSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrdersSerializer
    pagination_class = OrdersNumberPagination


class OrdersReadonlyViewSet(viewsets.ModelViewSet):
    queryset = OrderModel.objects.all()
    serializer_class = OrdersSerializer

    def get_queryset(self, *args, **kwargs):
        """
        获得queryset，参数中需含 P<uid> 参数，且设置basename
        :return:
        """
        uid = self.request.query_params.get("uid")
        return OrderModel.objects.filter(user_id=uid)


class OrderTransactionsViewSet(viewsets.ModelViewSet):
    serializer_class = OrderTransactionSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<order_id> 参数，且设置basename
        :return:
        """
        return OrderTransactionModel.objects.filter(order=self.kwargs['order_id'])


class OrderDetailsViewSet(viewsets.ModelViewSet):
    serializer_class = OrderDetailsSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<order_id> 参数，且设置basename
        :return:
        """
        return OrderDetailModel.objects.filter(order=self.kwargs['order_id'])


class OrderRoutesViewSet(viewsets.ModelViewSet):
    serializer_class = OrderRoutesSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<order_id> 参数，且设置basename
        :return:
        """
        return OrderRouteModel.objects.filter(order=self.kwargs['order_id'])


class OrderHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = OrderHistorySerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<order_id> 参数，且设置basename
        :return:
        """
        return OrdersHistoryModel.objects.filter(order=self.kwargs['order_id'])
