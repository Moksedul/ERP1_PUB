from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.urls import reverse
from products.models import Products
from organizations.models import Persons, Companies
from challan.models import Challan
from accounts.models import Accounts, default_account


def increment_buy_voucher_number():
    last_voucher = BuyVoucher.objects.all().order_by('id').last()
    if not last_voucher:
        return 'FEB-0001'
    voucher_number = last_voucher.voucher_number
    voucher_int = int(voucher_number.split('FEB-')[-1])
    new_voucher_int = voucher_int + 1
    new_voucher_no = ''
    if new_voucher_int < 10:
        new_voucher_no = 'FEB-000' + str(new_voucher_int)
    if 100 > new_voucher_int >= 10:
        new_voucher_no = 'FEB-00' + str(new_voucher_int)
    if 100 <= new_voucher_int < 1000:
        new_voucher_no = 'FEB-0' + str(new_voucher_int)
    if new_voucher_int >= 1000:
        new_voucher_no = 'FEB-' + str(new_voucher_int)
    return new_voucher_no


class BuyVoucher(models.Model):
    voucher_number = models.CharField(max_length=10, unique=True, default=increment_buy_voucher_number)
    seller_name = models.ForeignKey(Persons, on_delete=models.CASCADE, null=True)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    weight = models.FloatField(max_length=10)
    per_bag_unloading_cost = models.FloatField(blank=True, null=True)
    measuring_cost_per_kg = models.FloatField(blank=True, null=True)
    weight_of_each_bag = models.FloatField(blank=True, null=True)
    number_of_bag = models.FloatField(max_length=10)
    number_of_vehicle = models.IntegerField(blank=True, null=True)
    rate = models.FloatField(max_length=10)
    bazar_or_company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True)
    vehicle_plate_number = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateField(default=now)
    added_by = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    previous_amount = models.FloatField(blank=True, null=True, default=0)
    remarks = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.voucher_number)

    @staticmethod
    def get_absolute_url():
        return reverse('buy-list')


def increment_sale_number():
    last_voucher = SaleVoucher.objects.all().order_by('id').last()
    if not last_voucher:
        return 'FES-0001'
    voucher_number = last_voucher.voucher_number
    voucher_int = int(voucher_number.split('FES-')[-1])
    new_voucher_int = voucher_int + 1
    new_voucher_no = ''
    if new_voucher_int < 10:
        new_voucher_no = 'FES-000' + str(new_voucher_int)
    if 100 > new_voucher_int >= 10:
        new_voucher_no = 'FES-00' + str(new_voucher_int)
    if 100 <= new_voucher_int < 1000:
        new_voucher_no = 'FES-0' + str(new_voucher_int)
    if new_voucher_int >= 1000:
        new_voucher_no = 'FES-' + str(new_voucher_int)
    return new_voucher_no


class SaleVoucher(models.Model):
    voucher_number = models.CharField(max_length=10, unique=True, default=increment_sale_number)
    challan_no = models.ForeignKey(Challan, on_delete=models.CASCADE, null=True)
    per_bag_unloading_cost = models.FloatField(blank=True, null=True, default=0)
    measuring_cost_per_kg = models.FloatField(blank=True, null=True, default=0)
    weight_of_each_bag = models.FloatField(blank=True, null=True, default=0)
    rate = models.FloatField(max_length=10)
    date_added = models.DateField(default=now)
    added_by = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    status = models.BooleanField(default=False)
    remarks = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.voucher_number)

    @staticmethod
    def get_absolute_url():
        return reverse('sale-list')


def increment_general_voucher_number():
    last_voucher = GeneralVoucher.objects.all().order_by('id').last()
    if not last_voucher:
        return 'FEG-0001'
    voucher_number = last_voucher.voucher_number
    voucher_int = int(voucher_number.split('FEG-')[-1])
    new_voucher_int = voucher_int + 1
    new_voucher_no = ''
    if new_voucher_int < 10:
        new_voucher_no = 'FEG-000' + str(new_voucher_int)
    if 100 > new_voucher_int >= 10:
        new_voucher_no = 'FEG-00' + str(new_voucher_int)
    if 100 <= new_voucher_int < 1000:
        new_voucher_no = 'FEG-0' + str(new_voucher_int)
    if new_voucher_int >= 1000:
        new_voucher_no = 'FEG-' + str(new_voucher_int)
    return new_voucher_no


class GeneralVoucher(models.Model):
    voucher_number = models.CharField(max_length=10, unique=True, default=increment_general_voucher_number)
    person_name = models.CharField(max_length=200)
    cost_Descriptions = models.TextField(max_length=500, blank=True, null=True)
    cost_amount = models.FloatField()
    date_added = models.DateField(default=now)
    from_account = models.ForeignKey(
        Accounts, default=default_account(),
        null=True, blank=True, on_delete=models.CASCADE
    )
    remarks = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.voucher_number)

    @staticmethod
    def get_absolute_url():
        return reverse('general-voucher-list')
