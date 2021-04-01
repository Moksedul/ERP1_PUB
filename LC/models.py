from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from organizations.models import Bank
from products.models import Products


class LC(models.Model):
    lc_number = models.CharField(max_length=10, unique=True)
    bank_name = models.ForeignKey(Bank, on_delete=models.PROTECT)
    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    opening_date = models.DateField(default=now)
    date_time_stamp = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.lc_number)


class LCProduct(models.Model):
    name = models.ForeignKey(Products, on_delete=models.PROTECT)
    lc = models.ForeignKey(LC, on_delete=models.CASCADE)
    bags = models.FloatField(default=0)
    weight = models.FloatField()
    rate = models.FloatField()

    def __str__(self):
        return str(self.name)


class LCExpense(models.Model):
    name = models.CharField(max_length=50)
    lc = models.ForeignKey(LC, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return str(self.name)
