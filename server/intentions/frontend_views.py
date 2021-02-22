from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from intentions.mixins import *
from intentions.serializers import *


class IntentionsNumberPagination(PageNumberPagination):
    page_size = 8
    max_page_size = 50
    page_size_query_param = 'page_size'
    page_query_param = 'page'


class IntentionsViewSet(viewsets.ModelViewSet, IntentionCreateModelMixin):
    """
    留言订单视图集
    """
    queryset = IntentionsModel.objects.all()
    serializer_class = IntentionSerializer
    pagination_class = IntentionsNumberPagination

    @action(methods=['get'], detail=False, url_path='queryByUser')
    def get_intention_by_user(self, request):
        """
        获得queryset，参数中需含 P<uid> 参数，且设置basename
        :return:
        """
        uid = self.request.GET.get("wxid")
        res = IntentionsModel.objects.filter(wx_open_id=uid)
        intentions = IntentionSerializer(res, many=True).data
        intention_info = []
        for i in range(len(intentions)):
            details = IntentionDetailsModel.objects.filter(intention_id=intentions[i]['id'])
            intention_info.append(
                {"info": intentions[i], "detail": IntentionDetailsSerializer(details, many=True).data})
        return JsonResponse(intention_info, safe=False)

    def create(self, request, *args, **kwargs):
        return super().batch_create(request, *args, **kwargs)


class IntentionDetailsViewSet(viewsets.ModelViewSet):
    """
    留言订单商品清单视图集
    """
    serializer_class = IntentionDetailsSerializer

    # 序列化器选择
    def get_serializer_class(self):
        if self.action == 'create':
            return IntentionDetailsFrontSerializer
        if self.action == 'list':
            return IntentionDetailsSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<intention_id> 参数，且设置basename
        :return:
        """
        return IntentionDetailsModel.objects.filter(intention=self.kwargs['intention_id'])


class IntentionHistoryViewSet(viewsets.ModelViewSet):
    queryset = IntentionsHistoryModel.objects.all()
    serializer_class = IntentionHistorySerializer


class IntentionAssignmentsViewSet(viewsets.ModelViewSet):
    """
    留言订单分配视图集
    """
    queryset = IntentionAssignmentsModel.objects.all()
    serializer_class = IntentionAssignmentSerializer

    @action(methods=['get'], detail=False, url_path='queryByUser')
    def get_assignment(self, *args, **kwargs):
        """
        获得queryset，参数中需含 P<uid> 参数，且设置basename
        :return:
        """
        uid = self.request.GET.get("uid")
        user = UserModel.objects.get(id=uid)
        res = IntentionAssignmentsModel.objects.filter(user=user)
        body = IntentionAssignmentSerializer(res, many=True).data
        return JsonResponse(body, safe=False)

