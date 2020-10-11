from django.urls import path
from django.conf.urls import handler404
from .views import payment_report, collection_report, bkash_report

urlpatterns = [
    path('payment_report/', payment_report, name='payment-report'),
    path('collection_report/', collection_report, name='collection-report'),
    path('bkash_report/', bkash_report, name='bkash-report'),
]
