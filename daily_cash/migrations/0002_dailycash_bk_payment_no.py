# Generated by Django 3.0.6 on 2020-09-19 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bkash', '0009_auto_20200920_0047'),
        ('daily_cash', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailycash',
            name='bk_payment_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bkash.PaymentBkashAgent'),
        ),
    ]