from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from vouchers.models import BuyVoucher

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
    payment_date = models.DateTimeField(default=now)
    payment_mode = models.CharField(choices=PAYMENT_MODE_CHOICES, max_length=10)
    cheque_PO_TT_No = models.IntegerField(null=True, blank=True)
    cheque_date = models.DateField(default=now)
    bank_name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.payment_no)

