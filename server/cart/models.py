from django.db import models

from products.models import ProductModel
from users.models import UserModel


class CartModel(models.Model):
    """
    留言订单的商品明细表
    """
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, verbose_name='关联用户')
    product = models.ForeignKey(ProductModel, on_delete=models.DO_NOTHING, verbose_name='关联的产品')
    quantity = models.IntegerField(default=1, verbose_name='加购数量')

    class Meta:
        db_table = 'kh_cart'
