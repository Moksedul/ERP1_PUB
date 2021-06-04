from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from local_sale.models import LocalSale
from organizations.models import Persons

from django.contrib.auth.models import User
from accounts.models import Accounts
from vouchers.models import SaleVoucher

COLLECTION_MODE_CHOICES = [
    ('Cheque', 'Cheque'),
    ('Cash', 'Cash'),
    ('Online', 'Online'),
    ('Pay Order', 'Pay Order'),
]

SALE_TYPES = [
    ('SALE', 'SALE'),
    ('LOCAL SALE', 'LOCAL SALE'),
]


def increment_collection_number():
    last_collection = Collection.objects.all().order_by('id').last()
    if not last_collection:
        return 'FEC-0001'
    collection_number = last_collection.collection_no
    collection_int = int(collection_number.split('FEC-')[-1])
    new_collection_int = collection_int + 1
    new_collection_no = ''
    if new_collection_int < 10:
        new_collection_no = 'FEC-000' + str(new_collection_int)
    if 100 > new_collection_int >= 10:
        new_collection_no = 'FEC-00' + str(new_collection_int)
    if 100 <= new_collection_int < 1000:
        new_collection_no = 'FEC-0' + str(new_collection_int)
    if new_collection_int >= 1000:
        new_collection_no = 'FEC-' + str(new_collection_int)
    return new_collection_no


# Create your models here.
class Collection(models.Model):
    collection_no = models.CharField(max_length=10, unique=True, default=increment_collection_number)
    sale_type = models.CharField(max_length=10, choices=SALE_TYPES, default=SALE_TYPES[1])
    sale_voucher_no = models.ForeignKey(SaleVoucher, on_delete=models.CASCADE, null=True)
    local_sale_voucher_no = models.ForeignKey(LocalSale, on_delete=models.CASCADE, null=True)
    collected_by = models.ForeignKey(User, on_delete=models.CASCADE)
    collection_date = models.DateField(default=now)
    collection_mode = models.CharField(choices=COLLECTION_MODE_CHOICES, max_length=10)
    cheque_PO_ONL_no = models.IntegerField(null=True, blank=True)
    cheque_date = models.DateField(default=now, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    collection_amount = models.FloatField()
    collection_to_account = models.ForeignKey(Accounts, null=True, on_delete=models.CASCADE)
    collection_status = models.BooleanField(default=False)
    remarks = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.collection_no)

    @staticmethod
    def get_absolute_url():
        return reverse('collection-list')