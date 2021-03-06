# Generated by Django 3.1.2 on 2021-03-10 02:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('products', '0009_productmodel_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='加购数量')),
                ('product',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.productmodel',
                                   verbose_name='关联的产品')),
            ],
            options={
                'db_table': 'kh_cart',
            },
        ),
    ]
