# Generated by Django 3.1.4 on 2021-03-06 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0008_auto_20201207_0249'),
        ('payments', '0008_auto_20201205_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='voucher_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vouchers.buyvoucher'),
        ),
    ]
