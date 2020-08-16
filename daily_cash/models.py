from django.db import models
from payments.models import Payment


class DailyCash(models.Model):
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=50)
    voucher = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True, blank=True)
