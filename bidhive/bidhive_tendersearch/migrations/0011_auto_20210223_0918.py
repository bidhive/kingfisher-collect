# Generated by Django 3.1 on 2021-02-22 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bidhive_tendersearch', '0010_tender_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tender',
            old_name='procuring_entity',
            new_name='customer',
        ),
    ]
