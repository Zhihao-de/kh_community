# Generated by Django 3.0.3 on 2020-07-06 07:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intentions', '0002_intentiondetailsmodel_retail_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='intentionsmodel',
            options={'ordering': ['-id']},
        ),
    ]
