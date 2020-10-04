
from django.urls import path
from .views import *

urlpatterns = [
    path('ledger', ledger, name='ledger'),
    path('account_ledger', account_ledger_report, name='account-ledger'),
]