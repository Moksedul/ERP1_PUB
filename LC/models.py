from django.db import models
from accounts.models import Accounts


class LC(models.Model):
    lc_number = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=100)
    account = models.ForeignKey(Accounts, on_delete=models.PROTECT)