from django.db import models
from payments.models import Payment
from collection.models import Collection
from vouchers.models import *


class DailyCash(models.Model):
    date = models.DateField(auto_now=True)
    voucher = models.ForeignKey(Payment, GeneralVoucher, Collection, on_delete=models.DO_NOTHING, null=True, blank=True)
    description = models.TextField(max_length=1000)
    type = models.CharField(max_length=10)
