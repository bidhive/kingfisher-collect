# Generated by Django 3.1 on 2021-02-15 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidhive_tendersearch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tender',
            name='name',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='tender',
            name='publicationPolicy',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='tenderrelease',
            name='buyer',
            field=models.JSONField(null=True),
        ),
    ]
