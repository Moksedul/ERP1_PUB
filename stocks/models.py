from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from LC.models import LC
from hut_buy.models import HutBuy
from products.models import Products
from vouchers.models import BuyVoucher


class Stocks(models.Model):
    voucher_no = models.ForeignKey(BuyVoucher, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    weight_loss = models.FloatField(default=0)
    seed_weight = models.FloatField(default=0)
    spot_weight = models.FloatField(default=0)
    seed_rate = models.FloatField(default=0)
    spot_rate = models.FloatField(default=0)
    number_of_bag = models.FloatField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    remarks = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.product)

    @staticmethod
    def get_absolute_url():
        return reverse('stock-list')