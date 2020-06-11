# Generated by Django 3.0.6 on 2020-06-11 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vouchers', '0010_auto_20200528_1816'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0007_auto_20200611_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_no', models.CharField(max_length=50, unique=True)),
                ('payed_to', models.CharField(max_length=50)),
                ('payment_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('payment_mode', models.CharField(choices=[('CQ', 'Cheque'), ('CA', 'Cash'), ('ONL', 'Online'), ('PO', 'Pay Order')], max_length=10)),
                ('cheque_PO_ONL_no', models.IntegerField(blank=True, null=True)),
                ('cheque_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=50, null=True)),
                ('payment_amount', models.FloatField()),
                ('remarks', models.CharField(blank=True, max_length=50)),
                ('payed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('payment_from_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Accounts')),
                ('voucher_no', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vouchers.BuyVoucher')),
            ],
        ),
    ]
