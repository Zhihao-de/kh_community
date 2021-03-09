from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from orders.mixins import *
from orders.serizalizers import *


class OrdersNumberPagination(PageNumberPagination):
    page_size = 4
    max_page_size = 50
    page_size_query_param = 'page_size'
    page_query_param = 'page'


class OrdersViewSet(viewsets.ModelViewSet, OrderCreateModelMixin):
    queryset = OrderModel.objects.all()
    serializer_class = OrdersSerializer
    pagination_class = OrdersNumberPagination

    @action(methods=['get'], detail=False, url_path='queryByUser')
    def get_order_by_user(self, request):
        """
        获得queryset，参数中需含 P<uid> 参数，且设置basename
        :return:
        """
        uid = self.request.GET.get("user_id")
        res = OrderModel.objects.filter(user_id=uid)
        orders = OrdersSerializer(res, many=True).data
        order_info = []
        for i in range(len(orders)):
            details = OrderDetailModel.objects.filter(order_id=orders[i]['id'])
            order_info.append({"info": orders[i], "detail": OrderDetailsSerializer(details, many=True).data})
        return JsonResponse(order_info, safe=False)

    def create(self, request, *args, **kwargs):
        print("从这里进入")
        return super().batch_create(request, *args, **kwargs)


class OrderTransactionsViewSet(viewsets.ModelViewSet):
    queryset = OrderTransactionModel.objects.all()
    serializer_class = OrderTransactionSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<order_id> 参数，且设置basename
        :return:
        """
        return OrderTransactionModel.objects.filter(order=self.kwargs['order_id'])


class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetailModel.objects.all()
    serializer_class = OrderDetailsSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<order_id> 参数，且设置basename
        :return:
        """
        return OrderDetailModel.objects.filter(order=self.kwargs['order_id'])


class OrderRoutesViewSet(viewsets.ModelViewSet):
    queryset = OrderRouteModel.objects.all()
    serializer_class = OrderRoutesSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<order_id> 参数，且设置basename
        :return:
        """
        return OrderRouteModel.objects.filter(order=self.kwargs['order_id'])
