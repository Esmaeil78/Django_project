# Generated by Django 3.2.9 on 2021-12-21 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0005_alter_requestgoods_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestgoods',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyApp.profile', verbose_name='درخواست دهنده'),
        ),
    ]
