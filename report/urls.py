from django.urls import path
from .views import payment_report, collection_report


urlpatterns = [
    path('payment_report/', payment_report, name='payment-report'),
    path('collection_report/', collection_report, name='collection-report'),
]
