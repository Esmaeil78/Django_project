# Generated by Django 3.2.9 on 2021-12-10 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0003_auto_20211210_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationofgoods',
            name='code',
            field=models.CharField(error_messages={'unique': 'این کد قبلا وارد شده است'}, help_text='برای تولید خودکار کد کالا، رقم 1 را وارد کنید', max_length=15, unique=True, verbose_name='کد'),
        ),
    ]
