# Generated by Django 3.1.4 on 2021-05-15 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challan', '0011_challan_driver_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challan',
            name='driver_phone_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
