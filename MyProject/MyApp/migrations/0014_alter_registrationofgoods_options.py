# Generated by Django 3.2.9 on 2021-12-27 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0013_alter_registrationofgoods_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registrationofgoods',
            options={'ordering': ('code', 'name'), 'verbose_name': 'کالا', 'verbose_name_plural': 'کالا'},
        ),
    ]