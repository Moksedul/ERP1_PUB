# Generated by Django 3.2.8 on 2021-11-13 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0009_rename_rate_stock_rate_per_kg'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='weight_of_bags',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='stock',
            name='number_of_bag',
            field=models.FloatField(default=0),
        ),
    ]
