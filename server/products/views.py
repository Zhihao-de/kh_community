from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from products.serializers import *


# Create your views here.

class ProductsNumberPagination(PageNumberPagination):
    page_size = 4
    max_page_size = 50
    page_size_query_param = 'page_size'
    page_query_param = 'page'


class ProductsUnitNumberPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 25
    page_size_query_param = 'page_size'
    page_query_param = 'page'


class ProductCategoryReadonlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductCategoryModel.objects.all()
    serializer_class = ProductCategoriesReadonlySerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategoryModel.objects.all()
    serializer_class = ProductCategorySerializer

    @action(methods=['get'], detail=False)
    def list_tree(self, request, *args, **kwargs):
        """
        依据id和pid字段，将扁平数据转换为树形
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        items = super().list(request, args, kwargs).data
        res = {}
        for item in items:
            res.setdefault(item["id"], item).update(item)
            res.setdefault(item["parent"], {}).setdefault("children", []).append(item)
        if None in res:
            return Response(res[None]["children"], status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class ProductsReadonlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductModel.objects.filter(flags__in=[0])
    serializer_class = ProductsReadonlySerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductsSerializer
    pagination_class = ProductsNumberPagination
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['category']

    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class ProductUnitViewSet(viewsets.ModelViewSet):
    queryset = ProductUnitModel.objects.all()
    serializer_class = ProductUnitSerializer

    def get_queryset(self):
        """
        获得queryset，url中需含 P<order_id> 参数，且设置basename
        :return:
        """
        return ProductUnitModel.objects.filter(product=self.kwargs['product_id'])
