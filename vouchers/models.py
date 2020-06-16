from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from products.models import Products
from organizations.models import Persons, Companies


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


# Create your models here.
# RecordId,Name,ProductId,Weight,NumberOfBag,NumberOfVehicle,Rate,BazarOrCompanyName,VehicleNumberPlate,Date,Remarks
class BuyVoucher(models.Model):
    voucher_number = models.CharField(max_length=10, unique=True, default=increment_buy_voucher_number)
    seller_name = models.ForeignKey(Persons, on_delete=models.CASCADE, null=True)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    weight = models.FloatField(max_length=10)
    number_of_bag = models.FloatField(max_length=10)
    number_of_vehicle = models.IntegerField(blank=True, null=True)
    rate = models.FloatField(max_length=10)
    bazar_or_company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True)
    vehicle_plate_number = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateTimeField(default=now)
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
    buyer_name = models.ForeignKey(Persons, on_delete=models.CASCADE, null=True)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    weight = models.FloatField(max_length=10)
    number_of_bag = models.FloatField(max_length=10)
    number_of_vehicle = models.IntegerField(blank=True, null=True)
    rate = models.FloatField(max_length=10)
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True)
    vehicle_plate_number = models.CharField(max_length=50, blank=True, null=True)
    driver_name = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateTimeField(default=now)
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
    date_added = models.DateTimeField(default=now)
    remarks = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.voucher_number)

    @staticmethod
    def get_absolute_url():
        return reverse('general-voucher-list')