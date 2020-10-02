
from django.urls import path
from .views import *

urlpatterns = [
    path('ledger', index, name='ledger'),
    path('account_ledger', account_ledger_report, name='account-ledger'),
    path('report_daily_cash/<int:selected_account>/', account_ledger_report, name='report-daily-cash'),
]