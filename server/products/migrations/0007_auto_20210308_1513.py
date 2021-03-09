# Generated by Django 3.1.2 on 2021-03-08 07:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0006_auto_20210301_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmodel',
            name='purchase_price',
        ),
        migrations.AddField(
            model_name='productmodel',
            name='purchase_Price_corporate',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='加盟用户价格'),
        ),
        migrations.AddField(
            model_name='productmodel',
            name='purchase_price_register',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='注册用户价格'),
        ),
    ]
