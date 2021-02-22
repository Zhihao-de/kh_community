from django.core.cache import cache
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from intentions.models import IntentionsModel, IntentionDetailsModel, IntentionsHistoryModel
from products.models import ProductModel

"""
#class IntentionAssignmentsBatchCreateModelMixin:
  
    Create a model instance.
    
    def batch_create(self, request, *args, **kwargs):
        print("这就是请求的数据")
        print(request.data)
        serializers = [self.get_serializer(data=data) for data in request.data]
        for serializer in serializers:
            print(serializer)
            serializer.is_valid(raise_exception=True)
        self.perform_batch_create(serializers, args)
        headers = self.get_success_headers(serializers[0].data)

        return Response(list([serializer.data for serializer in serializers]),
                        status=status.HTTP_201_CREATED, headers=headers)

    def perform_batch_create(self, serializers, *args):
        with transaction.atomic():
            for serializer in serializers:
                serializer.save()
            # change the flags to ASSIGNED

            IntentionsModel.objects.filter(id=args[0][1]['intention_id']).update(flags=1)

    def get_success_headers(self, data):
        try:
            print("请求 header")
            print(data)
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class IntentionAssignmentsBatchUpdateModelMixin:
  
    Update a model instance.
    

    def batch_update(self, request, *args, **kwargs):
        serializers = [
            self.get_serializer(IntentionAssignmentsModel.objects.get(id=data['id']), data=data, partial=True)
            for data in request.data]
        for serializer in serializers:
            serializer.is_valid(raise_exception=True)
        self.perform_batch_update(serializers, args)
        return Response(list([serializer.data for serializer in serializers]))

    def perform_batch_update(self, serializers, *args):
        with transaction.atomic():
            for serializer in serializers:
                serializer.save()
            # change the flags to UNASSIGNED
            IntentionsModel.objects.filter(id=args[0][1]['intention_id']).update(flags=0)
    """


class IntentionCreateModelMixin:
    """
    Create a model instance.
    """

    def batch_create(self, request, *args, **kwargs):
        # intention的serializer
        serializer = self.get_serializer(data=request.data)
        details = request.data.pop("details")
        serializer.is_valid(raise_exception=True)

        # 在这里save
        self.perform_batch_create(serializer, details, args)
        headers = self.get_success_headers(serializer.data)
        return Response(list([detail for detail in details]),
                        status=status.HTTP_201_CREATED, headers=headers)

    def perform_batch_create(self, serializer, details, *args):
        with transaction.atomic():
            # save intentionModel
            res = serializer.save()
            # add details
            intention = IntentionsModel.objects.get(id=res.id)

            for detail in details:
                if 'checked' in detail:
                    detail.pop('checked')

            # 这里先放着因为单位不清楚  最好单位统一为克，能够进行统一换算
            # total_weight = Decimal(0).quantize('0.00')
            total_weight = 0
            for detail in details:
                product_id = detail.pop('product')["id"]
                quantity = int(detail['quantity'])
                product = ProductModel.objects.get(id=product_id)
                total_weight = total_weight + quantity * product.weight
                IntentionDetailsModel.objects.create(intention=intention, product=product,
                                                     retail_price=product.retail_price, **detail)
            # 保存intention的重量
            intention.weight = total_weight
            intention.save()
            # 保存intention的历史
            IntentionsHistoryModel.objects.create(serial_number=intention.serial_number, quantity=intention.quantity,
                                                  weight=intention.weight, flags=intention.flags,
                                                  created_at=intention.created_at, updated_at=intention.created_at,
                                                  wx_open_id=intention.wx_open_id, wx_union_id=intention.wx_union_id,
                                                  wx_name=intention.wx_name, wx_avatar_url=intention.wx_avatar_url,
                                                  name=intention.name, phone=intention.phone, country=intention.country,
                                                  province=intention.province, city=intention.city,
                                                  address=intention.address, postcode=intention.postcode,
                                                  message=intention.postcode, intention=intention)


    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


"""
class IntentionPatchModelMixin:
  
 

    def patch(self, request, *args, **kwargs):
        # intention的serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            # 保存数据
            res = serializer.save()
            intention = IntentionsModel.objects.get(id=res.id)
            # 增加历史记录
            IntentionsHistoryModel.objects.create(serial_number=intention.serial_number, quantity=intention.quantity,
                                                  weight=intention.weight, flags=intention.flags,
                                                  created_at=intention.created_at, updated_at=intention.created_at,
                                                  wx_open_id=intention.wx_open_id, wx_union_id=intention.wx_union_id,
                                                  wx_name=intention.wx_name, wx_avatar_url=intention.wx_avatar_url,
                                                  name=intention.name, phone=intention.phone, country=intention.country,
                                                  province=intention.province, city=intention.city,
                                                  address=intention.address, postcode=intention.postcode,
                                                  message=intention.postcode, intention=intention)
            headers = self.get_success_headers(serializer.data)
            return Response(status=status.HTTP_200_OK, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}
"""
