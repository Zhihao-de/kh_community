# Generated by Django 3.1.2 on 2021-03-08 07:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0010_auto_20210107_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='flags',
            field=models.SmallIntegerField(
                choices=[(0, '已申请'), (1, '待签协议'), (2, '已注册'), (3, '暂停'), (4, '普通用户'), (5, '加盟用户')],
                verbose_name='用户状态'),
        ),
    ]
