from django.urls import path
from django.views.i18n import JavaScriptCatalog
from .views import *

urlpatterns = [
    path('add_buy_voucher', BuyVoucherCreateView.as_view(), name='add-buy-voucher'),
    path('add_person_buy', PersonCreateBuy.as_view(), name='add-person-buy'),
    path('buy_list', BuyListView.as_view(), name='buy-list'),
    path('buy/<int:pk>/detail', buy_details, name='buy-detail'),
    path('buy/<int:pk>/update', BuyVoucherUpdateView.as_view(), name='buy-update'),
    path('buy/<int:pk>/delete', BuyDeleteView.as_view(), name='buy-delete'),
    path('add_sale', sale_create, name='add-sale'),
    path('sale_list', SaleListView.as_view(), name='sale-list'),
    path('sale/<int:pk>/update', sale_update, name='sale-update'),
    path('sale/<int:pk>/delete', SaleDeleteView.as_view(), name='sale-delete'),
    path('sale/<int:pk>/detail', sale_details, name='sale-detail'),
    path('add_general_voucher', GeneralVoucherCreateView.as_view(), name='add-general-voucher'),
    path('general_voucher/<int:pk>/update', GeneralVoucherUpdateView.as_view(), name='general-voucher-update'),
    path('general_voucher_list', GeneralVoucherListView.as_view(), name='general-voucher-list'),
    path('general_voucher/<int:pk>/delete', GeneralVoucherDeleteView.as_view(), name='general-voucher-delete'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
