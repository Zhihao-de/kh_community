# Generated by Django 3.1.2 on 2021-03-09 07:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0014_ordermodel_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='freight',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14, verbose_name='运费'),
        ),
    ]
