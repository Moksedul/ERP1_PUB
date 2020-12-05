from django.urls import path
from .views import *
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('add_payment', PaymentCreate.as_view(), name='add-payment'),
    path('payment/add_person', PersonCreatePayment.as_view(), name='add-person-payment'),
    path('load_buy_vouchers/', load_buy_vouchers, name='load-buy-vouchers'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('payment_list', PaymentListView.as_view(), name='payment-list'),
    path('payment/<int:pk>/detail', payment_details, name='payment-detail'),
    path('payment/<int:pk>/update', PaymentUpdateView.as_view(), name='payment-update'),
    path('payment/<int:pk>/delete', PaymentDeleteView.as_view(), name='payment-delete'),
    path('payment_search/', payment_search, name='payment-search'),
]
