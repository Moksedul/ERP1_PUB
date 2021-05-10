from django.db import models
from django.utils.timezone import now
from django.urls import reverse
from django.contrib.auth.models import User


def default_account():
    account = Accounts.objects.get(account_name='Daily Cash').pk
    return account


class Accounts(models.Model):
    account_name = models.CharField(max_length=50, null=True, default='M/S FATEMA ENTERPRISE')
    account_no = models.CharField(max_length=50, null=True, unique=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)
    bank_branch = models.CharField(max_length=50, null=True, blank=True)
    date_added = models.DateTimeField(default=now, blank=True)
    remarks = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.account_name

    @staticmethod
    def get_absolute_url():
        return reverse('bank-account-list')


class Investment(models.Model):
    source_of_investment = models.CharField(max_length=200, default='Daily Cash Invest')
    investing_amount = models.FloatField()
    investing_to_account = models.ForeignKey(
        Accounts, default=default_account, null=True, on_delete=models.CASCADE, related_name='investing_to_account'
    )
    investing_from_account = models.ForeignKey(Accounts, on_delete=models.CASCADE,
                                               null=True, blank=True, related_name='investing_from_account')
    added_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=now, blank=True)
    date = models.DateField(default=now)
    remarks = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.source_of_investment

    @staticmethod
    def get_absolute_url():
        return reverse('investment-list')
