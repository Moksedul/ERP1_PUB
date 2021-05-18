from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from LC.models import LC
from hut_buy.models import HutBuy
from products.models import Products
from vouchers.models import BuyVoucher


class Stocks(models.Model):
    lc = models.ForeignKey(LC, on_delete=models.CASCADE)
    buy = models.ForeignKey(BuyVoucher, on_delete=models.CASCADE)
    hut_buy = models.ForeignKey(HutBuy, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Products, on_delete=models.CASCADE)
    weight_loss = models.FloatField()
    seed_weight = models.FloatField()
    spot_weight = models.FloatField()
    seed_rate = models.FloatField()
    spot_rate = models.FloatField()
    number_of_bag = models.FloatField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    remarks = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.room_no)

    @staticmethod
    def get_absolute_url():
        return reverse('stock-list')