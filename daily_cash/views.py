from django.shortcuts import render
from .models import DailyCash


def create(data):
    daily_cash = DailyCash(payment_voucher=1, name='Physics', max_marks=100)
    print(data)

