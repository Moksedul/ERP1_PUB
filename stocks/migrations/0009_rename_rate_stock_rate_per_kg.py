# Generated by Django 3.2.8 on 2021-11-11 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0008_stock_rate_per_mann'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='rate',
            new_name='rate_per_kg',
        ),
    ]