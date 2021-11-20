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
    business_name = models.ForeignKey(Organization, on_delete=models.Empty, blank=True, null=True)
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
    added_to_finished_stock = models.BooleanField(default=False)
    remarks = models.CharField(max_length=225, blank=True)

    def __str__(self):
        return str(self.product)

    @property
    def details(self):
        from core.views import stock_details
        return stock_details(self.pk)

    @staticmethod
    def get_absolute_url():
        return reverse('pre-stock-list')


class FinishedStock(models.Model):
    business_name = models.ForeignKey(Organization, on_delete=models.Empty, blank=True, null=True)
    store_name = models.ForeignKey(Store, on_delete=models.Empty, blank=True, null=True)
    pre_stock = models.ForeignKey(PreStock, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.PROTECT)
    buying_rate_per_kg = models.FloatField(default=0)
    processing_cost_per_kg = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    number_of_bag = models.FloatField(default=0)
    date_time_stamp = models.DateTimeField(auto_now_add=True, null=True)
    last_updated_time = models.DateTimeField(auto_now=True, null=True)
    added_by = CurrentUserField(related_name='finished_stock_added_by')
    updated_by = CurrentUserField(on_update=True, related_name='finished_stock_updated_by')
    inventory_updated = models.BooleanField(default=False)
    remarks = models.CharField(max_length=225, blank=True)

    class Meta:
        unique_together = [("product", "pre_stock")]

    def __str__(self):
        return str(self.product)

    @property
    def details(self):
        return '0'

    @staticmethod
    def get_absolute_url():
        return reverse('finished-stock-list')

