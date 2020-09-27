from django.db import models
from django.utils.timezone import now

from organizations.models import Persons, Companies
from products.models import Products


def increment_local_sale_no():
    last_voucher = LocalSale.objects.all().order_by('id').last()
    if not last_voucher:
        return 'FELS-0001'
    voucher_number = last_voucher.voucher_number
    voucher_int = int(voucher_number.split('FELS-')[-1])
    new_voucher_int = voucher_int + 1
    new_voucher_no = ''
    if new_voucher_int < 10:
        new_voucher_no = 'FELS-000' + str(new_voucher_int)
    if 100 > new_voucher_int >= 10:
        new_voucher_no = 'FELS-00' + str(new_voucher_int)
    if 100 <= new_voucher_int < 1000:
        new_voucher_no = 'FELS-0' + str(new_voucher_int)
    if new_voucher_int >= 1000:
        new_voucher_no = 'FELS-' + str(new_voucher_int)
    return new_voucher_no


class LocalSale(models.Model):
    sale_no = models.CharField(max_length=10, default=increment_local_sale_no)
    buyer_name = models.ForeignKey(Persons, on_delete=models.SET_NULL, null=True)
    company_name = models.ForeignKey(Companies, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=now)
    date_time_stamp = models.DateTimeField(default=now)


class Product(models.Model):
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    sale_no = models.ForeignKey(LocalSale, on_delete=models.CASCADE)
    rate = models.FloatField()
    weight = models.FloatField()



