# Generated by Django 3.0.3 on 2020-06-12 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntentionAssignmentsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(blank=True, max_length=255, verbose_name='备注')),
                ('flags', models.SmallIntegerField(choices=[(0, '正常'), (1, '超时'), (2, '删除'), (3, '完成')], default=0, verbose_name='分配状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='分配时间')),
            ],
            options={
                'db_table': 'kh_intention_assignments',
            },
        ),
        migrations.CreateModel(
            name='IntentionDetailsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='订购数量')),
            ],
            options={
                'db_table': 'kh_intention_details',
            },
        ),
        migrations.CreateModel(
            name='IntentionsHistoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wx_open_id', models.CharField(max_length=255)),
                ('wx_name', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=16)),
                ('phone', models.CharField(max_length=16)),
                ('country', models.CharField(max_length=255)),
                ('province', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=255)),
                ('flags', models.SmallIntegerField(choices=[(0, '待分配'), (1, '已分配'), (2, '已完成'), (3, '已取消'), (4, '无法联系')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'kh_intentions_history',
            },
        ),
        migrations.CreateModel(
            name='IntentionsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=255, verbose_name='留言订单编号')),
                ('quantity', models.SmallIntegerField(default=0, verbose_name='商品数量')),
                ('flags', models.SmallIntegerField(choices=[(0, '待分配'), (1, '已分配'), (2, '已完成'), (3, '已取消'), (4, '无法联系')], verbose_name='订单状态')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('wx_open_id', models.CharField(max_length=255, verbose_name='微信openid')),
                ('wx_union_id', models.CharField(max_length=255, verbose_name='微信unionid')),
                ('wx_name', models.CharField(max_length=255, verbose_name='微信名')),
                ('wx_avatar_url', models.CharField(max_length=255, null=True, verbose_name='微信头像URL')),
                ('wx_mobile', models.CharField(max_length=11, null=True, verbose_name='手机号')),
                ('name', models.CharField(max_length=16, verbose_name='客户姓名')),
                ('phone', models.CharField(max_length=16, verbose_name='客户联系电话')),
                ('country', models.CharField(default='中国', max_length=255, verbose_name='客户国籍')),
                ('province', models.CharField(max_length=255, verbose_name='客户所在省份')),
                ('city', models.CharField(max_length=255, verbose_name='客户所在城市')),
                ('address', models.CharField(max_length=255, verbose_name='客户详细地址')),
                ('postcode', models.CharField(max_length=255, verbose_name='客户地址的邮政编码')),
                ('message', models.TextField(blank=True, verbose_name='客户留言')),
                ('products', models.ManyToManyField(through='intentions.IntentionDetailsModel', to='products.ProductModel', verbose_name='商品列表')),
                ('users', models.ManyToManyField(through='intentions.IntentionAssignmentsModel', to='users.UserModel', verbose_name='分配的用户')),
            ],
            options={
                'db_table': 'kh_intentions',
            },
        ),
        migrations.AddField(
            model_name='intentiondetailsmodel',
            name='intention',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intentions.IntentionsModel', verbose_name='关联的留言订单'),
        ),
        migrations.AddField(
            model_name='intentiondetailsmodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.ProductModel', verbose_name='关联的产品'),
        ),
        migrations.CreateModel(
            name='IntentionDetailsHistoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=1.0, max_digits=14)),
                ('retail_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=14)),
                ('intention', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intentions.IntentionsHistoryModel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.ProductModel')),
            ],
            options={
                'db_table': 'kh_intention_details_history',
            },
        ),
        migrations.AddField(
            model_name='intentionassignmentsmodel',
            name='intention',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intentions.IntentionsModel', verbose_name='关联的留言订单'),
        ),
        migrations.AddField(
            model_name='intentionassignmentsmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.UserModel', verbose_name='关联的用户'),
        ),
    ]
