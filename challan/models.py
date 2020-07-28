from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
from products.models import Products
from organizations.models import Persons, Companies


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
    buyer_name = models.ForeignKey(Persons, on_delete=models.CASCADE, null=True)
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    weight = models.FloatField(max_length=10)
    number_of_bag = models.FloatField(max_length=10)
    number_of_vehicle = models.IntegerField(blank=True, null=True)
    name_of_driver = models.CharField(max_length=200, blank=True, null=True)
    vehicle_plate_number = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateTimeField(default=now)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.challan_no)

    @staticmethod
    def get_absolute_url():
        return reverse('challan-list')