# Generated by Django 3.1 on 2021-02-23 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidhive_tendersearch', '0011_auto_20210223_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tender',
            name='contract_value',
            field=models.BigIntegerField(null=True),
        ),
    ]
