from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import User
from vouchers.models import BuyVoucher
from accounts.models import Accounts

PAYMENT_MODE_CHOICES = [
    ('CQ', 'Cheque'),
    ('CA', 'Cash'),
    ('ONL', 'Online'),
    ('PO', 'Pay Order'),
]


def increment_payment_number():
    last_payment = Payment.objects.all().order_by('id').last()
    if not last_payment:
        return 'FEP-0001'
    payment_number = last_payment.payment_no
    payment_int = int(payment_number.split('FEP-')[-1])
    new_payment_int = payment_int + 1
    new_payment_no = ''
    if new_payment_int < 10:
        new_payment_no = 'FEP-000' + str(new_payment_int)
    if 100 > new_payment_int >= 10:
        new_payment_no = 'FEP-00' + str(new_payment_int)
    if 100 <= new_payment_int < 1000:
        new_payment_no = 'FEP-0' + str(new_payment_int)
    if new_payment_int >= 1000:
        new_payment_no = 'FEP-' + str(new_payment_int)
    return new_payment_no


class Payment(models.Model):
    payment_no = models.CharField(max_length=50, unique=True, default=increment_payment_number)
    voucher_no = models.ForeignKey(BuyVoucher, null=True, blank=True, on_delete=models.CASCADE)
    payed_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    payed_to = models.CharField(max_length=50)
    payment_date = models.DateField(default=now, null=True, blank=True)
    payment_mode = models.CharField(choices=PAYMENT_MODE_CHOICES, max_length=10)
    cheque_PO_ONL_no = models.IntegerField(null=True, blank=True)
    cheque_date = models.DateField(default=now, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    payment_amount = models.FloatField()
    payment_from_account = models.ForeignKey(Accounts, null=True, on_delete=models.CASCADE, blank=True)
    remarks = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.payment_no)

    @staticmethod
    def get_absolute_url():
        return reverse('payment-list')