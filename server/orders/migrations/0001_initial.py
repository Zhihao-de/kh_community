# Generated by Django 3.0.3 on 2020-06-12 06:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=255, verbose_name='订单编号')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='订单金额')),
                ('quantity', models.SmallIntegerField(default=0, verbose_name='商品数量')),
                ('name', models.CharField(max_length=16, verbose_name='收货人姓名')),
                ('phone', models.CharField(max_length=16, verbose_name='收货人联系电话')),
                ('country', models.CharField(default='中国', max_length=255, verbose_name='收货人国籍')),
                ('province', models.CharField(max_length=255, verbose_name='收货人所在省份')),
                ('city', models.CharField(max_length=255, verbose_name='收货人所在城市')),
                ('address', models.CharField(max_length=255, verbose_name='收货人详细地址')),
                ('postcode', models.CharField(max_length=255, verbose_name='收货人地址的邮政编码')),
                ('message', models.TextField(blank=True, verbose_name='收货人备注')),
                ('flags', models.SmallIntegerField(choices=[(0, '未付款'), (1, '已付款'), (2, '配送中'), (3, '已签收'), (4, '已取消'), (5, '已退款')], default=0, verbose_name='订单状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.UserModel', verbose_name='关联用户')),
            ],
            options={
                'db_table': 'kh_orders',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderTransactionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='支付金额')),
                ('payment_method', models.SmallIntegerField(choices=[(0, '支付宝'), (1, '微信支付'), (2, '银行卡'), (3, '其他')], default=1, verbose_name='支付方式')),
                ('transaction_id', models.CharField(default='00000000000000000000000000000000', max_length=64, verbose_name='交易ID')),
                ('paid_at', models.DateTimeField(null=True, verbose_name='付款时间')),
                ('refund', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='投款金额')),
                ('refunded_at', models.DateTimeField(null=True, verbose_name='退款时间')),
                ('status', models.CharField(max_length=255, null=True, verbose_name='交易状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrderModel', verbose_name='关联订单')),
            ],
            options={
                'db_table': 'kh_order_transactions',
            },
        ),
        migrations.CreateModel(
            name='OrdersHistoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=14)),
                ('tare', models.DecimalField(decimal_places=2, default=0.0, max_digits=14)),
                ('payment_method', models.SmallIntegerField(choices=[(0, '支付宝'), (1, '微信支付'), (2, '银行卡'), (3, '其他')], default=1)),
                ('is_paid', models.BooleanField(blank=True, default=True)),
                ('transaction_id', models.CharField(default='00000000000000000000000000000000', max_length=64)),
                ('paid_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('refund', models.DecimalField(decimal_places=2, default=0.0, max_digits=14)),
                ('flags', models.SmallIntegerField(choices=[(0, '未付款'), (1, '已付款'), (2, '配送中'), (3, '已签收'), (4, '已取消'), (5, '已退款')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.UserModel')),
            ],
            options={
                'db_table': 'kh_orders_history',
            },
        ),
        migrations.CreateModel(
            name='OrderRouteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('express', models.CharField(max_length=32, verbose_name='物流服务名称')),
                ('receipt_no', models.CharField(max_length=255, unique=True, verbose_name='物流单号')),
                ('address', models.CharField(max_length=512, verbose_name='发货地址')),
                ('quantity', models.IntegerField(default=0, verbose_name='数量')),
                ('weight', models.DecimalField(decimal_places=3, default=0.0, max_digits=14, verbose_name='总重千克')),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='运费')),
                ('remark', models.TextField(blank=True, verbose_name='备注')),
                ('routes', models.TextField(blank=True, verbose_name='物流郭晨')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrderModel', verbose_name='关联订单')),
            ],
            options={
                'db_table': 'kh_order_routes',
            },
        ),
        migrations.CreateModel(
            name='OrderDetailsHistoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('weight', models.DecimalField(decimal_places=3, default=0.0, max_digits=14)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrdersHistoryModel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.ProductModel')),
            ],
            options={
                'db_table': 'kh_order_details_history',
            },
        ),
        migrations.CreateModel(
            name='OrderDetailModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='交易单价元')),
                ('quantity', models.IntegerField(default=0, verbose_name='商品数量')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrderModel', verbose_name='关联订单')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.ProductModel', verbose_name='关联产品')),
            ],
            options={
                'db_table': 'kh_order_details',
            },
        ),
    ]
