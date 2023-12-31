# Generated by Django 3.2.9 on 2022-01-08 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0025_alter_requestgoods_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrygoods',
            name='time',
            field=models.TimeField(auto_now_add=True, null=True, verbose_name='ساعت ورود'),
        ),
        migrations.AddField(
            model_name='exitgoods',
            name='time',
            field=models.TimeField(auto_now_add=True, null=True, verbose_name='ساعت خروج'),
        ),
    ]