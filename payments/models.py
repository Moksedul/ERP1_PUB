from django.db import models
from django.utils.timezone import now
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime
from django.contrib.auth.models import User
from vouchers.models import BuyVoucher
from accounts.models import Accounts

PAYMENT_MODE_CHOICES = [
    ('CQ', 'Cheque'),
    ('CA', 'Cash'),
    ('ONL', 'Online'),
    ('PO', 'Pay Order'),
]


class Payment(models.Model):
    payment_no = models.CharField(max_length=50, unique=True)
    voucher_no = models.ForeignKey(BuyVoucher, null=True, on_delete=models.CASCADE)
    payed_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    payed_to = models.CharField(max_length=50)
    payment_date = models.DateField(default=now, null=True, blank=True)
    payment_mode = models.CharField(choices=PAYMENT_MODE_CHOICES, max_length=10)
    cheque_PO_ONL_no = models.IntegerField(null=True, blank=True)
    cheque_date = models.DateField(default=now, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    payment_amount = models.FloatField()
    payment_from_account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.payment_no)

