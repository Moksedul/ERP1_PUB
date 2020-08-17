from django.db import models
from payments.models import Payment
from collection.models import Collection
from vouchers.models import *


class DailyCash(models.Model):
    date = models.DateField(auto_now=True)
    payment_voucher = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    collection_voucher = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True)
    general_voucher = models.ForeignKey(GeneralVoucher, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=1000)
    debit = models.FloatField(default=0.0)
    credit = models.FloatField(default=0.0)
