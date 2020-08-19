from django.db import models
from payments.models import Payment
from collection.models import Collection
from vouchers.models import *
from accounts.models import Investment


class DailyCash(models.Model):
    date = models.DateField(auto_now=True)
    general_voucher = models.ForeignKey(GeneralVoucher, on_delete=models.CASCADE, null=True, blank=True)
    payment_no = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
    collection_no = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True)
    investment_no = models.ForeignKey(Investment, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=1000)
    type = models.CharField(max_length=1)
