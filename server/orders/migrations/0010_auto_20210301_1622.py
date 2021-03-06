# Generated by Django 3.1.2 on 2021-03-01 08:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0006_auto_20210301_1448'),
        ('orders', '0009_auto_20210106_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetailmodel',
            name='productUnit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='products.productunitmodel', verbose_name='关联产品SKU'),
        ),
        migrations.AddField(
            model_name='orderdetailshistorymodel',
            name='productUnit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='products.productunitmodel', verbose_name='关联产品SKU'),
        ),
    ]
