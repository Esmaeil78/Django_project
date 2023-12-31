# Generated by Django 3.2.9 on 2022-01-19 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0034_auto_20220119_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrygoods',
            name='id',
            field=models.IntegerField(error_messages={'unique': 'این شناسه قبلا وارد شده است'}, help_text='این شناسه توسط سرور تولید شده است.', primary_key=True, serialize=False, unique=True, verbose_name='شناسه ورود'),
        ),
        migrations.AlterField(
            model_name='exitgoods',
            name='id',
            field=models.IntegerField(error_messages={'unique': 'این شناسه قبلا وارد شده است'}, help_text='این شناسه توسط سرور تولید شده است.', primary_key=True, serialize=False, unique=True, verbose_name='شناسه خروج'),
        ),
    ]