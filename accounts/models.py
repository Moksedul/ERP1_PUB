from django.db import models
from django.urls import reverse
from django.contrib.auth.models import


class BankAccounts(models.Model):
    account_name = models.CharField(max_length=50, null=True, default='M/S FATEMA ENTERPRISE')
    account_no = models.CharField(max_length=50, null=True, unique=True)
    bank_name = models.CharField(max_length=50, null=True)
    bank_branch = models.CharField(max_length=50, null=True)
    opening_balance = models.FloatField(null=True, default=0)
    remarks = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.account_name

    @staticmethod
    def get_absolute_url():
        return reverse('bank-account-list')


class OtherAccounts(models.Model):
    account_name = models.CharField(max_length=50, null=True, default='CASH IN HAND', unique=True)
    opening_balance = models.FloatField(null=True, default=0)
    remarks = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.account_name

    @staticmethod
    def get_absolute_url():
        return reverse('other-account-list')


class Investment(models.Model):
    source_of_investment = models.CharField(max_length=200)
    investing_amount = models.FloatField()
    investing_to_account = models.ForeignKey(BankAccounts, OtherAccounts, null=True)
    added_by = models.ForeignKey()
    remarks = models.CharField(max_length=200)