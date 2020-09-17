from django.db import models


# Create your models here.
class BkashAgents:
    agent_name = models.CharField(max_length=50)
    agent_number = models.IntegerField(max_length=11, unique=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    contact_name = models.CharField(max_length=50, null=True, blank=True)
    contact_no = models.IntegerField(max_length=14, null=True, blank=True)
    remarks = models.CharField(max_length=200, null=True, blank=True)


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


class BkashTransaction:
    invoice_no = models.CharField()
