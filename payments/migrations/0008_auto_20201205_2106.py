# Generated by Django 3.0.6 on 2020-12-05 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0006_auto_20201008_1508'),
        ('payments', '0007_auto_20201005_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='voucher_no',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vouchers.BuyVoucher'),
        ),
    ]