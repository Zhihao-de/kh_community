from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.deconstruct import deconstructible
from rest_framework import serializers
from rest_framework.utils.formatting import lazy_format

from products.models import ProductModel, ProductCategoryModel, ProductUnitModel


class ProductCategoriesReadonlySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryModel
        ordering = ['order']
        exclude = ['created_at']


class ProductsReadonlySerializer(serializers.ModelSerializer):
    weight = serializers.FloatField()
    purchase_price = serializers.FloatField()
    retail_price = serializers.FloatField()
    flags = serializers.CharField(source='get_flags_display')

    class Meta:
        model = ProductModel
        fields = '__all__'


@deconstructible
class PkUrlValidator:
    def __call__(self, value):
        value = str(value)
        if ',' not in value:
            raise ValidationError(self.messages['invalid'])
        pk, url = value.split(',')
        if not pk.isdigit() or int(pk) < 1:
            raise ValidationError('invalid pk')
        uv = URLValidator()
        uv(url)


class IdUrlField(serializers.CharField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        message = lazy_format(self.error_messages['invalid'])
        self.validators.append(PkUrlValidator(message=message))


class IdUrlListField(serializers.ListField):
    def to_representation(self, data):
        """
        List of object instances -> List of dicts of primitive datatypes.
        """
        if isinstance(data, str):
            print(data)
            data = eval(data)
        return [self.child.to_representation(item) if item is not None else None for item in data]


class ProductCategorySerializer(serializers.ModelSerializer):
    pic_url = IdUrlListField(child=IdUrlField(), allow_empty=True)

    class Meta:
        model = ProductCategoryModel
        fields = ["id", "name", "description", "pic_url", "order", "parent"]


class ProductsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_blank=True)
    description = serializers.CharField(allow_blank=True)
    pic_url = IdUrlListField(child=IdUrlField(), allow_empty=True)
    carousal_urls = IdUrlListField(child=IdUrlField(), allow_empty=True)
    weight = serializers.FloatField()
    purchase_price = serializers.FloatField()
    retail_price = serializers.FloatField()

    class Meta:
        model = ProductModel
        fields = '__all__'


class ProductUnitSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    purchase_price = serializers.FloatField()
    retail_price = serializers.FloatField()
    weight = serializers.FloatField()
    unit = serializers.CharField()
    point = serializers.IntegerField()
    attributes = serializers.CharField()
    description = serializers.CharField(allow_blank=True)

    class Meta:
        model = ProductUnitModel
        fields = '__all__'
