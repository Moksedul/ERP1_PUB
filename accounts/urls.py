from django.urls import path
from .views import *


urlpatterns = [
    path('accounts', home, name='accounts'),
    path('add_bank_account', BankAccountCreate.as_view(), name='add-bank-account'),
    path('bank_account_list', BankAccountList.as_view(), name='bank-account-list'),
    path('bank_account/<int:pk>/update', BankAccountUpdate.as_view(), name='bank-account-update'),
    path('bank_account/<int:pk>/delete', BankAccountDelete.as_view(), name='bank-account-delete'),
    path('add_other_account', OtherAccountCreate.as_view(), name='add-other-account'),
    path('other_account_list', OtherAccountList.as_view(), name='other-account-list'),
    path('other_account/<int:pk>/update', OtherAccountUpdate.as_view(), name='other-account-update'),
    path('other_account/<int:pk>/delete', OtherAccountDelete.as_view(), name='other-account-delete'),
    path('add_investment', InvestmentCreateView.as_view(), name='add-investment'),
    path('investment_list', InvestmentList.as_view(), name='investment-list'),
    path('investment/<int:pk>/delete/', delete_investment, name='investment-delete'),
]
