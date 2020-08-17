from django.db import models
from payments.models import Payment
from collection.models import
from vouchers.models import *


class DailyCash(models.Model):
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=50)
    payment_voucher = models.ForeignKey(Payment, on_delete=models.CASCADE)
    collection_voucher = models.ForeignKey()