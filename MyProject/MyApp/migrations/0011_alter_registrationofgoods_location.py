# Generated by Django 3.2.9 on 2021-12-25 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0010_alter_selectwarehouse_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationofgoods',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MyApp.location', verbose_name='محل استقرار'),
        ),
    ]
