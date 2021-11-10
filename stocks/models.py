from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from LC.models import LC
from hut_buy.models import HutBuy
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
    rate = models.FloatField(default=0)
    number_of_bag = models.FloatField(blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    remarks = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return str(self.product)

    @staticmethod
    def get_absolute_url():
        return reverse('stock-list')