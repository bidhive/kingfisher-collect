# Generated by Django 3.1 on 2021-02-17 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidhive_tendersearch', '0005_auto_20210217_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='tender',
            name='deadline_date',
            field=models.DateTimeField(null=True),
        ),
    ]
