from django.db import models


class AccountLedger(models.Model):
    date = models.DateField(auto_now=True)
    voucher = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=10)