from django.shortcuts import render
from .models import DailyCash


def create_daily_cash(data):
    daily_cash = DailyCash(general_voucher=data['voucher'], description=data['description'], type=data['type'])
    # daily_cash.save()
    print(daily_cash)

