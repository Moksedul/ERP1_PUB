from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from products.models import Products
from organizations.models import Persons, Companies, Organization


# model for challan

def increment_challan_number():
    last_challan = Challan.objects.all().order_by('id').last()
    if not last_challan:
        return 'FEC-0001'
    challan_number = last_challan.challan_no
    challan_int = int(challan_number.split('FEC-')[-1])
    new_challan_int = challan_int + 1
    new_challan_no = ''
    if new_challan_int < 10:
        new_challan_no = 'FEC-000' + str(new_challan_int)
    if 100 > new_challan_int >= 10:
        new_challan_no = 'FEC-00' + str(new_challan_int)
    if 100 <= new_challan_int < 1000:
        new_challan_no = 'FEC-0' + str(new_challan_int)
    if new_challan_int >= 1000:
        new_challan_no = 'FEC-' + str(new_challan_int)
    return new_challan_no


class Challan(models.Model):
    challan_no = models.CharField(max_length=10, unique=True, default=increment_challan_number)
    reference = models.CharField(max_length=50)
    business_name = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True)
    sub_dealer = models.ForeignKey(Persons, on_delete=models.Empty, null=True, blank=True)
    challan_serial = models.CharField(max_length=10, unique=True, null=True)
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    weight_adjusted = models.FloatField(max_length=10)
    weight_of_each_bag = models.FloatField(default=0)
    number_of_bag = models.FloatField(max_length=10)
    number_of_vehicle = models.IntegerField(blank=True, null=True)
    name_of_driver = models.CharField(max_length=200, blank=True, null=True)
    driver_phone_no = models.CharField(max_length=20, null=True, blank=True)
    vehicle_plate_number = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateTimeField(auto_now=True)
    challan_date = models.DateField(default=now)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.challan_no) + "-" + str(self.challan_serial)

    @staticmethod
    def get_absolute_url():
        return reverse('challan-list')

    @property
    def total_weight(self):
        bag_no = self.number_of_bag
        bag_weight = self.weight_of_each_bag
        adjust = self.weight_adjusted
        total = (bag_no * bag_weight) + adjust

        return round(total, 2)