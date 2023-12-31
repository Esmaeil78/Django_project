# Generated by Django 3.2.9 on 2022-01-13 12:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0030_auto_20220110_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrygoods',
            name='SerialForDriver',
            field=models.CharField(blank=True, help_text='شماره رسید انبا = تاریخ امروز+شناسه کاربری راننده+شماره ورود راننده', max_length=50, verbose_name='شماره رسید انبار'),
        ),
        migrations.AlterField(
            model_name='exitgoods',
            name='SerialForDriver',
            field=models.CharField(blank=True, help_text='شماره حواله انبار = تاریخ امروز+شناسه کاربری راننده+شماره خروج راننده', max_length=50, verbose_name='شماره حواله انبار'),
        ),
        migrations.AlterField(
            model_name='requestgoods',
            name='serial',
            field=models.PositiveIntegerField(blank=True, help_text='حداکثر 11 رقم', null=True, validators=[django.core.validators.MaxValueValidator(99999999999, 'کد رهگیری وارد شده باید حداکثر دارای 11 رقم باشد!')], verbose_name='کد رهگیری(شناسه خروج)'),
        ),
        migrations.AlterField(
            model_name='warehousehandling',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات'),
        ),
    ]
