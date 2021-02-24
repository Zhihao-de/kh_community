# Generated by Django 3.1.2 on 2021-02-24 07:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic_url', models.CharField(default='[]', max_length=255, verbose_name='商品图片链接')),
                ('purchase_price',
                 models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='采购价元')),
                (
                'retail_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='指导价元')),
                ('weight', models.DecimalField(decimal_places=3, default=0.0, max_digits=14, verbose_name='重量')),
                ('unit', models.CharField(max_length=32, verbose_name='重量单位')),
                ('point', models.IntegerField(default=0, verbose_name='单品积分')),
                ('flags', models.SmallIntegerField(choices=[(0, '在售'), (1, '已售')], verbose_name='商品状态')),
                ('product',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.productmodel',
                                   verbose_name='产品spu')),
            ],
            options={
                'db_table': 'kh_product_unit',
                'ordering': ['flags'],
            },
        ),
    ]
