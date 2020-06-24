# Generated by Django 3.0.6 on 2020-05-25 05:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import vouchers.models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_auto_20200524_0013'),
        ('products', '0002_auto_20200521_1621'),
        ('vouchers', '0007_auto_20200524_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyvoucher',
            name='number_of_vehicle',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='buyvoucher',
            name='vehicle_plate_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='SaleVoucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_number', models.CharField(default=vouchers.models.increment_buy_voucher_number, max_length=10, unique=True)),
                ('weight', models.FloatField(max_length=10)),
                ('number_of_bag', models.FloatField(max_length=10)),
                ('number_of_vehicle', models.IntegerField(blank=True, null=True)),
                ('rate', models.FloatField(max_length=10)),
                ('vehicle_plate_number', models.CharField(blank=True, max_length=50, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('remarks', models.CharField(blank=True, max_length=500)),
                ('buyer_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Persons')),
                ('company_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.Companies')),
                ('product_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Products')),
            ],
        ),
    ]