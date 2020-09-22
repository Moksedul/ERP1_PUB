from django.db import models
from organizations.models import Persons, Companies


def increment_local_sale_no():
    last_voucher = LocalSale.objects.all().order_by('id').last()
    if not last_voucher:
        return 'FELS-0001'
    voucher_number = last_voucher.voucher_number
    voucher_int = int(voucher_number.split('FELS-')[-1])
    new_voucher_int = voucher_int + 1
    new_voucher_no = ''
    if new_voucher_int < 10:
        new_voucher_no = 'FELS-000' + str(new_voucher_int)
    if 100 > new_voucher_int >= 10:
        new_voucher_no = 'FELS-00' + str(new_voucher_int)
    if 100 <= new_voucher_int < 1000:
        new_voucher_no = 'FELS-0' + str(new_voucher_int)
    if new_voucher_int >= 1000:
        new_voucher_no = 'FELS-' + str(new_voucher_int)
    return new_voucher_no


# class Product(models.Model):
#     product_name = models.CharField(max_length=50)
#     rate = models.FloatField()
#
#
# class LocalSale(models.Model):
#     local_sale_no = models.CharField(max_length=10, default=increment_local_sale_no)
#     buyer_name = models.ForeignKey(Persons, on_delete=models.SET_NULL, null=True)
#     company_name = models.ForeignKey(Companies, on_delete=models.SET_NULL, null=True)
