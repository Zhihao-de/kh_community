from django.db import models


# Create your models here.


class ProductCategoryModel(models.Model):
    """
    商品分类表
    """
    name = models.CharField(max_length=255, verbose_name='类别名称')
    description = models.CharField(max_length=1024, blank=True, verbose_name='说明')
    pic_url = models.CharField(max_length=255, default='[]', verbose_name='类别图片')
    order = models.IntegerField(default=0, verbose_name='显示顺序')
    parent = models.ForeignKey('ProductCategoryModel', on_delete=models.DO_NOTHING, null=True, verbose_name='父级商品分类')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kh_product_categories'
        ordering = ['order']


class ProductModel(models.Model):
    """
    商品表
    """
    category = models.ForeignKey(ProductCategoryModel, on_delete=models.DO_NOTHING, verbose_name='商品分类')
    name = models.CharField(max_length=255, verbose_name='商品名称')
    title = models.CharField(max_length=255, blank=True, verbose_name='副标题')
    pic_url = models.CharField(max_length=255, default='[]', verbose_name='商品图片链接')
    carousal_urls = models.CharField(max_length=1024, default='[]', verbose_name='轮播图片集合')
    description = models.TextField(blank=True, verbose_name='商品说明')
    weight = models.DecimalField(max_digits=14, decimal_places=3, default=0.000, verbose_name='重量')
    unit = models.CharField(max_length=32, verbose_name='重量单位')
    purchase_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name='采购价元')
    retail_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name='指导价元')
    stock = models.IntegerField(default=0, verbose_name='库存')
    flags = models.SmallIntegerField(choices=[
        (0, '在售'),
        (1, '售罄'),
        (2, '编辑'),
        (3, '作废'),
    ], verbose_name='商品状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'kh_products'
        ordering = ['flags']


class ProductUnitModel(models.Model):
    """
    商品单品SKU
    """
    code = models.CharField(max_length=32, verbose_name='单品编号')
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING, verbose_name='产品spu')
    # pic_url = models.CharField(max_length=255, default='[]', verbose_name='商品图片链接')
    purchase_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name='采购价元')
    retail_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name='指导价元')
    weight = models.DecimalField(max_digits=14, decimal_places=3, default=0.000, verbose_name='重量')
    unit = models.CharField(max_length=32, verbose_name='重量单位')
    point = models.IntegerField(default=0, verbose_name='单品积分')
    attributes = models.CharField(max_length=255, verbose_name='单品规格')
    description = models.CharField(max_length=255, verbose_name='单品描述')
    flags = models.SmallIntegerField(choices=[
        (0, '在售'),
        (1, '已售')
    ], verbose_name='商品状态')

    class Meta:
        db_table = 'kh_product_unit'
        ordering = ['code']
