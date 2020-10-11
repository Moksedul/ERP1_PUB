from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from organizations.models import Persons, Companies
from products.models import Products


def increment_local_sale_no():
    last_voucher = LocalSale.objects.all().order_by('id').last()
    if not last_voucher:
        return 'FELS-0001'
    voucher_number = last_voucher.sale_no
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


PAYEE = [
    ('CUSTOMER', 'CUSTOMER'),
    ('SUPPLIER', 'SUPPLIER'),
]


class LocalSale(models.Model):
    sale_no = models.CharField(max_length=10, default=increment_local_sale_no, unique=True)
    buyer_name = models.ForeignKey(Persons, on_delete=models.SET_NULL, null=True)
    company_name = models.ForeignKey(Companies, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=now)
    transport_charge = models.FloatField(default=0, blank=True)
    transport_charge_payee = models.CharField(choices=PAYEE, default=PAYEE[1], max_length=8, blank=True)
    previous_due = models.FloatField(default=0, blank=True)
    date_time_stamp = models.DateTimeField(default=now)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    discount = models.FloatField(default=0, blank=True)
    remarks = models.CharField(max_length=200, default='N/A', null=True, blank=True)

    def __str__(self):
        return str(self.sale_no)


class Product(models.Model):
    name = models.ForeignKey(Products, on_delete=models.CASCADE)
    sale_no = models.ForeignKey(LocalSale, on_delete=models.CASCADE)
    rate = models.FloatField()
    weight = models.FloatField()
    number_of_bag = models.FloatField(default=0)

    def __str__(self):
        return str(self.name)
