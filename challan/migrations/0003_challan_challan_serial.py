# Generated by Django 3.1.4 on 2021-05-08 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challan', '0002_challan_challan_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='challan',
            name='challan_serial',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]