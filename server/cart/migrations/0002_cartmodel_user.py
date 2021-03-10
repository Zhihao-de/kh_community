# Generated by Django 3.1.2 on 2021-03-10 03:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0012_auto_20210309_1055'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartmodel',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='users.usermodel',
                                    verbose_name='关联用户'),
            preserve_default=False,
        ),
    ]
