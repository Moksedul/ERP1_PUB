from django.contrib.auth.models import User
from django.db import models

from accounts.models import Accounts, default_account
from organizations.models import Persons
from django.urls import reverse
from django.utils.timezone import now


class BkashAgents(models.Model):
    agent_name = models.CharField(max_length=50)
    agent_number = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    contact_name = models.CharField(max_length=50, null=True, blank=True)
    contact_no = models.CharField(max_length=14, null=True, blank=True)
    remarks = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.agent_name)

    @staticmethod
    def get_absolute_url():
        return reverse('agent-list')


def increment_invoice_number():
    last_invoice = BkashTransaction.objects.all().order_by('id').last()
    if not last_invoice:
        return 'FEBK-0001'
    invoice_number = last_invoice.invoice_no
    invoice_int = int(invoice_number.split('FEBK-')[-1])
    new_invoice_int = invoice_int + 1
    new_payment_no = ''
    if new_invoice_int < 10:
        new_payment_no = 'FEBK-000' + str(new_invoice_int)
    if 100 > new_invoice_int >= 10:
        new_payment_no = 'FEBK-00' + str(new_invoice_int)
    if 100 <= new_invoice_int < 1000:
        new_payment_no = 'FEBK-0' + str(new_invoice_int)
    if new_invoice_int >= 1000:
        new_payment_no = 'FEBK-' + str(new_invoice_int)
    return new_payment_no


TRANSACTION_AGAINST = [
    ('GENERAL', 'GENERAL'),
    ('PAYMENT', 'PAYMENT'),
    # ('SALARY', 'SALARY'),
]


class BkashTransaction(models.Model):
    invoice_no = models.CharField(max_length=10, default=increment_invoice_number, unique=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_AGAINST, default=TRANSACTION_AGAINST[0])
    payed_to = models.ForeignKey(Persons, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=50, null=True, blank=True)
    agent_name = models.ForeignKey(BkashAgents, on_delete=models.CASCADE)
    transaction_phone_no = models.CharField(max_length=11)
    transaction_amount = models.FloatField()
    transaction_ID = models.CharField(max_length=14, null=True, blank=True)
    transaction_date = models.DateField(default=now)
    date_time_stamp = models.DateTimeField(default=now)
    description = models.TextField(max_length=200, null=True, blank=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.invoice_no)


def increment_payment_number():
    last_payment = PaymentBkashAgent.objects.all().order_by('id').last()
    if not last_payment:
        return 'FEBKP-0001'
    payment_number = last_payment.payment_no
    payment_int = int(payment_number.split('FEBKP-')[-1])
    new_payment_int = payment_int + 1
    new_payment_no = ''
    if new_payment_int < 10:
        new_payment_no = 'FEBKP-000' + str(new_payment_int)
    if 100 > new_payment_int >= 10:
        new_payment_no = 'FEBKP-00' + str(new_payment_int)
    if 100 <= new_payment_int < 1000:
        new_payment_no = 'FEBKP-0' + str(new_payment_int)
    if new_payment_int >= 1000:
        new_payment_no = 'FEBKP-' + str(new_payment_int)
    return new_payment_no


class PaymentBkashAgent(models.Model):
    payment_no = models.CharField(max_length=10, default=increment_payment_number, unique=True)
    transaction_invoice_no = models.ForeignKey(BkashTransaction, on_delete=models.SET_NULL, null=True, blank=True)
    agent_name = models.ForeignKey(BkashAgents, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    description = models.TextField(max_length=200, null=True, blank=True)
    payment_date = models.DateField(default=now)
    payment_from_account = models.ForeignKey(Accounts, on_delete=models.CASCADE, default=default_account)
    date_time_stamp = models.DateTimeField(default=now)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.payment_no)

    @staticmethod
    def get_absolute_url():
        return reverse('agent-payment-list')
