# Generated by Django 3.2.9 on 2021-12-23 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0007_auto_20211224_0203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exitgoods',
            options={'default_permissions': ('add',), 'ordering': ('warehouse__name', '-date'), 'verbose_name': 'خروج کالا', 'verbose_name_plural': 'خروج کالا'},
        ),
    ]
