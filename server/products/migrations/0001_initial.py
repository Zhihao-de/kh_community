# Generated by Django 3.0.3 on 2020-06-12 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='类别名称')),
                ('description', models.CharField(blank=True, max_length=1024, verbose_name='说明')),
                ('pic_url', models.CharField(default='[]', max_length=255, verbose_name='类别图片')),
                ('order', models.IntegerField(default=0, verbose_name='显示顺序')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.ProductCategoryModel', verbose_name='父级商品分类')),
            ],
            options={
                'db_table': 'kh_product_categories',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='商品名称')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='副标题')),
                ('pic_url', models.CharField(default='[]', max_length=255, verbose_name='商品图片链接')),
                ('carousal_urls', models.CharField(default='[]', max_length=1024, verbose_name='轮播图片集合')),
                ('description', models.TextField(blank=True, verbose_name='商品说明')),
                ('weight', models.DecimalField(decimal_places=3, default=0.0, max_digits=14, verbose_name='重量')),
                ('unit', models.CharField(max_length=32, verbose_name='重量单位')),
                ('purchase_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='采购价元')),
                ('retail_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='指导价元')),
                ('stock', models.IntegerField(default=0, verbose_name='库存')),
                ('flags', models.SmallIntegerField(choices=[(0, '在售'), (1, '售罄'), (2, '编辑'), (3, '作废')], verbose_name='商品状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.ProductCategoryModel', verbose_name='商品分类')),
            ],
            options={
                'db_table': 'kh_products',
                'ordering': ['flags'],
            },
        ),
    ]
