# Generated by Django 3.2.9 on 2022-01-19 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0035_auto_20220120_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestgoods',
            name='address',
            field=models.TextField(verbose_name='ادر'),
        ),
    ]
