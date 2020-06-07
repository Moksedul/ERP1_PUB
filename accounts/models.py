from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Accounts(models.Model):
    account_name = models.CharField(max_length=50, null=True, default='M/S FATEMA ENTERPRISE')
    account_no = models.CharField(max_length=50, null=True, unique=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    bank_branch = models.CharField(max_length=50, null=True, blank=True)
    opening_balance = models.FloatField(null=True, default=0)
    remarks = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.account_name

    @staticmethod
    def get_absolute_url():
        return reverse('bank-account-list')


class Investment(models.Model):
    source_of_investment = models.CharField(max_length=200)
    investing_amount = models.FloatField()
    investing_to_account = models.ForeignKey(Accounts, null=True, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.source_of_investment

    @staticmethod
    def get_absolute_url():
        return reverse('bank-account-list')


