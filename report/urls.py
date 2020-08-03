from django.urls import path
from .views_ajax import *
from .views import *


urlpatterns = [
    path('report_buy/', payment_search, name='report-buy'),
]
