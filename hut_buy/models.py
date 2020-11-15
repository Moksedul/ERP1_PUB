from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from products.models import Products


class HutBuy(models.Model):
    hut_name = models.CharField(max_length=20)
    date = models.DateField(default=now)
    posted_by = models.ForeignKey(User, on_delete=models.PROTECT)
    date_time_stamp = models.DateTimeField(auto_now=True)


class HutProduct(models.Model):
    name = models.ForeignKey(Products, on_delete=models.CASCADE)
    hut_buy = models.ForeignKey(HutBuy, on_delete=models.CASCADE)
    weight = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return str(self.name)


class Expense(models.Model):
    name = models.ForeignKey(Products, on_delete=models.CASCADE)
    hut_buy = models.ForeignKey(HutBuy, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return str(self.name)