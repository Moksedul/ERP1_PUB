from django.urls import path
from ledger.views import account_ledger_report
from .views import *


urlpatterns = [
    path('report_buy/', payment_search, name='report-buy'),
]
