from django.urls import path
from .views import PaymentCreate


urlpatterns = [
    path('add_payment', PaymentCreate.as_view(), name='add-payment'),
]
