# Generated by Django 3.2.8 on 2021-12-06 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0023_remove_prestock_added_to_processing_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finishedstock',
            name='processing_cost_per_kg',
        ),
    ]
