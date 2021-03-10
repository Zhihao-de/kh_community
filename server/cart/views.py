from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from cart.mixin import CartCreateModelMixin, CartPatchModelMixin
from cart.models import CartModel
from cart.serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet, CartCreateModelMixin, CartPatchModelMixin):
    queryset = CartModel.objects.all()
    serializer_class = CartSerializer

    @action(methods=['get'], detail=False, url_path='queryByUser')
    def get_intention_by_user(self, request):
        """
        获得queryset，参数中需含 P<uid> 参数，且设置basename
        :return:
        """
        uid = self.request.GET.get("uid")
        res = CartModel.objects.filter(user_id=uid)
        carts = CartSerializer(res, many=True).data

        return JsonResponse(carts, safe=False)

    # 增加一条记录
    def create(self, request, *args, **kwargs):
        return super().batch_create(request, *args, **kwargs)

    # 更新一条记录
    def update(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
