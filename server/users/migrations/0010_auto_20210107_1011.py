# Generated by Django 3.0.3 on 2021-01-07 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210106_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddressmodel',
            name='district',
            field=models.CharField(max_length=255, verbose_name='收件人地区'),
        ),
    ]
