from django.shortcuts import render
from .models import DailyCash


def create_daily_cash(data):
    daily_cash = DailyCash(
        general_voucher=data['general_voucher'],
        description=data['description'],
        type=data['type'],
        payment_no=data['payment_no'],
        collection_no=data['collection_no'],
        investment_no=data['investment_no']
    )
    daily_cash.save()
    print(daily_cash)
