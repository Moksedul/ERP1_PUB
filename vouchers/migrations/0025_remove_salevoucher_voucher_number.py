# Generated by Django 3.0.6 on 2021-10-27 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0024_remove_buyvoucher_voucher_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salevoucher',
            name='voucher_number',
        ),
    ]