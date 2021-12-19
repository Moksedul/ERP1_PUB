from django.db import models
from django.urls import reverse
from django_currentuser.db.models import CurrentUserField

from organizations.models import Organization
from products.models import Products
from vouchers.models import BuyVoucher


class Store(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.name)


class PreStock(models.Model):
    voucher_no = models.ForeignKey(BuyVoucher, on_delete=models.CASCADE, null=True, blank=True)
    store_name = models.ForeignKey(Store, on_delete=models.Empty, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    weight_adjustment = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    rate_per_kg = models.FloatField(default=0)
    rate_per_mann = models.FloatField(default=0)
    number_of_bag = models.FloatField(default=0)
    weight_of_bags = models.FloatField(default=0)
    date_time_stamp = models.DateTimeField(auto_now_add=True, null=True)
    last_updated_time = models.DateTimeField(auto_now=True, null=True)
    added_by = CurrentUserField(related_name='stock_added_by')
    updated_by = CurrentUserField(on_update=True, related_name='stock_updated_by')
    # added_to_processing_stock = models.BooleanField(default=False)
    added_to_finished_stock = models.BooleanField(default=False)
    remarks = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return str(self.product)

    @property
    def details(self):
        from core.views import stock_details
        return stock_details(self.pk)

    @property
    def added_to_processing_stock(self):
        processing_stock = ProcessingStock.objects.filter(pre_stocks__id=self.id)
        if processing_stock:
            return True
        else:
            return False

    @staticmethod
    def get_absolute_url():
        return reverse('pre-stock-list')


class ProcessingStock(models.Model):
    pre_stocks = models.ManyToManyField(PreStock)
    date_time_stamp = models.DateTimeField(auto_now_add=True, null=True)
    last_updated_time = models.DateTimeField(auto_now=True, null=True)
    added_by = CurrentUserField(related_name='processing_stock_added_by')
    updated_by = CurrentUserField(on_update=True, related_name='processing_stock_updated_by')
    processing_completed = models.BooleanField(default=False)
    remarks = models.CharField(max_length=225, blank=True)

    def __str__(self):
        product_name = self.pre_stocks.all().first()
        return str(product_name)

    @property
    def product(self):
        product_name = self.pre_stocks.all().first()
        return product_name

    @property
    def vouchers(self):
        pre_stocks = self.pre_stocks.all()
        vouchers = []
        for pre_stock in pre_stocks:
            if pre_stock.voucher_no:
                vouchers.append(pre_stock.voucher_no.voucher_number)
        return list(dict.fromkeys(vouchers))

    @property
    def business(self):
        pre_stocks = self.pre_stocks.all()
        business = []
        for pre_stock in pre_stocks:
            if pre_stock.voucher_no:
                business.append(pre_stock.voucher_no.business_name.name)
        return list(dict.fromkeys(business))

    @property
    def weight(self):
        initial_weight = 0
        pre_stocks = self.pre_stocks.all()

        for pre_stock in pre_stocks:
            initial_weight += pre_stock.details['net_weight']

        post_stocks = PostStock.objects.filter(processing_stock_id=self.pk)
        remaining_weight = initial_weight

        for post_stock in post_stocks:
            remaining_weight -= post_stock.weight

        weight = {
            'initial_weight': initial_weight,
            'remaining_weight': remaining_weight,
        }
        return weight

    @property
    def details(self):
        return '0'

    @property
    def serial(self):
        from core.views import serial_gen
        return serial_gen(self.id, 'PROS')

    @staticmethod
    def get_absolute_url():
        return reverse('processing-stock-list')


class PostStock(models.Model):
    processing_stock = models.ForeignKey(ProcessingStock, on_delete=models.CASCADE)
    business_name = models.ForeignKey(Organization, on_delete=models.Empty)
    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    weight = models.FloatField(default=0)
    rate_per_kg = models.FloatField(default=0)
    bags = models.FloatField(default=0)
    is_finished = models.BooleanField(default=False)
    store = models.ForeignKey(Store, on_delete=models.Empty, null=True)


class FinishedStock(models.Model):
    business_name = models.ForeignKey(Organization, on_delete=models.Empty, blank=True, null=True)
    store_name = models.ForeignKey(Store, on_delete=models.Empty, blank=True, null=True)
    processing_stock = models.ForeignKey(ProcessingStock, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    rate_per_kg = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    number_of_bag = models.FloatField(default=0)
    date_time_stamp = models.DateTimeField(auto_now_add=True, null=True)
    last_updated_time = models.DateTimeField(auto_now=True, null=True)
    added_by = CurrentUserField(related_name='finished_stock_added_by')
    updated_by = CurrentUserField(on_update=True, related_name='finished_stock_updated_by')
    inventory_updated = models.BooleanField(default=False)
    remarks = models.CharField(max_length=225, blank=True)

    class Meta:
        unique_together = [("product", "processing_stock")]

    def __str__(self):
        return str(self.product)

    @property
    def details(self):
        return '0'

    @staticmethod
    def get_absolute_url():
        return reverse('finished-stock-list')

