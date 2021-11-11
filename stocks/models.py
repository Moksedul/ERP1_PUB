from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField

from products.models import Products
from vouchers.models import BuyVoucher


class Store(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.name)


class Stock(models.Model):
    voucher_no = models.ForeignKey(BuyVoucher, on_delete=models.CASCADE, null=True, blank=True)
    store_name = models.ForeignKey(Store, on_delete=models.Empty, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    weight_adjustment = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    rate_per_kg = models.FloatField(default=0)
    rate_per_mann = models.FloatField(default=0)
    number_of_bag = models.FloatField(blank=True, null=True)
    date_time_stamp = models.DateTimeField(auto_now_add=True, null=True)
    last_updated_time = models.DateTimeField(auto_now=True, null=True)
    added_by = CurrentUserField(related_name='stock_added_by')
    updated_by = CurrentUserField(on_update=True, related_name='stock_updated_by')
    remarks = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return str(self.product)

    @property
    def total_weight(self):
        total_weight = self.weight + self.weight_adjustment
        return total_weight

    @property
    def total_amount(self):
        total_weight = self.weight + self.weight_adjustment
        total_amount = total_weight * self.rate
        return total_amount

    @staticmethod
    def get_absolute_url():
        return reverse('stock-list')
