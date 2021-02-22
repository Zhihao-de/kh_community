from django.db.models import Q
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from intentions.serializers import *


class IntentionsNumberPagination(PageNumberPagination):
    page_size = 4
    max_page_size = 50
    page_size_query_param = 'page_size'
    page_query_param = 'page'


# ViewSet
class IntentionsReadonlyViewSet(viewsets.ModelViewSet):
    queryset = IntentionsModel.objects.all()
    serializer_class = IntentionSerializer
    pagination_class = IntentionsNumberPagination

    def get_queryset(self, *args, **kwargs):
        """
        获得queryset，参数中需含 P<open_id> 参数，且设置basename
        :return:
        """
        wxid = self.request.query_params.get("wxid")
        return IntentionsModel.objects.filter(wx_open_id=wxid)


# IntentionViewSet
class IntentionsViewSet(viewsets.ModelViewSet):
    """
    留言订单视图集
    """
    queryset = IntentionsModel.objects.all()
    serializer_class = IntentionSerializer
    pagination_class = IntentionsNumberPagination



class IntentionDetailsViewSet(viewsets.ModelViewSet):
    """
    留言订单商品清单视图集
    """
    serializer_class = IntentionDetailsSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<intention_id> 参数，且设置basename
        :return:
        """
        return IntentionDetailsModel.objects.filter(intention=self.kwargs['intention_id'])


class IntentionAssignmentsViewSet(viewsets.ModelViewSet):
    """
    留言订单分配视图集
    """
    serializer_class = IntentionAssignmentSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<intention_id> 参数，且设置basename
        :return:
        """
        return IntentionAssignmentsModel.objects.filter(Q(intention=self.kwargs['intention_id']) & ~Q(flags=2))


class IntentionAssignmentsDropViewSet(viewsets.ModelViewSet):
    """
    专门用来删除分配结果
    """
    queryset = IntentionAssignmentsModel.objects.all()
    serializer_class = IntentionAssignmentSerializer


class IntentionHistoryViewSet(viewsets.ModelViewSet):
    """
    用来操作intention的历史记录
    """
    serializer_class = IntentionHistorySerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<intention_id> 参数，且设置basename
        :return:
        """
        return IntentionsHistoryModel.objects.filter(Q(intention=self.kwargs['intention_id']) & ~Q(flags=2))
