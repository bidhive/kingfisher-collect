# Generated by Django 3.1 on 2021-02-19 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidhive_tendersearch', '0006_tender_deadline_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tender',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='tender',
            name='tender_id',
            field=models.CharField(max_length=1024, null=True, unique=True),
        ),
    ]
