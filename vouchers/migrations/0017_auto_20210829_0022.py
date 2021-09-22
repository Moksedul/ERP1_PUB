# Generated by Django 3.0.6 on 2021-08-28 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0016_buyvoucher_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyvoucher',
            name='transport_cost',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='buyvoucher',
            name='transport_cost_payee',
            field=models.CharField(choices=[('Seller', 'Seller'), ('Buyer', 'Buyer')], default='Buyer', max_length=10),
        ),
    ]