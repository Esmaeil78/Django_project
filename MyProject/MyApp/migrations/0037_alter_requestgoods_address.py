# Generated by Django 3.2.9 on 2022-01-19 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0036_alter_requestgoods_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestgoods',
            name='address',
            field=models.TextField(verbose_name='ادرس'),
        ),
    ]
