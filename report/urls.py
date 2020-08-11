from django.urls import path
from .views import *


urlpatterns = [
    path('report_buy/', payment_search, name='report-buy'),
    path('report_accounts/', account_report_index, name='report-accounts'),
    path('report_daily_cash/', daily_cash_report, name='report-daily-cash'),
]
