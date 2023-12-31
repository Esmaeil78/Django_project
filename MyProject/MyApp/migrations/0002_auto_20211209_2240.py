# Generated by Django 3.2.9 on 2021-12-09 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entrygoods',
            options={'ordering': ('warehouse__name',), 'verbose_name': 'ورود کالا', 'verbose_name_plural': 'ورود کالا'},
        ),
        migrations.AlterModelOptions(
            name='exitgoods',
            options={'ordering': ('warehouse__name',), 'verbose_name': 'خروج کالا', 'verbose_name_plural': 'خروج کالا'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ('warehouse__name',), 'verbose_name': 'محل استقرار', 'verbose_name_plural': 'محل استقرار'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('post',), 'verbose_name': 'پروفایل', 'verbose_name_plural': 'پروفایل'},
        ),
        migrations.AlterModelOptions(
            name='registrationofgoods',
            options={'ordering': ('code',), 'verbose_name': 'کالا', 'verbose_name_plural': 'کالا'},
        ),
        migrations.AlterModelOptions(
            name='requestgoods',
            options={'ordering': ('profile__user__username',), 'verbose_name': 'درخواست کالا', 'verbose_name_plural': 'درخواست کالا'},
        ),
        migrations.AlterModelOptions(
            name='warehouse',
            options={'ordering': ('company__name',), 'verbose_name': 'انبار', 'verbose_name_plural': 'انبار'},
        ),
    ]
