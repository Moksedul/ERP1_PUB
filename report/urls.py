from django.urls import path
from .views import payment_report


urlpatterns = [
    path('payment_report/', payment_report, name='payment-report'),
]
