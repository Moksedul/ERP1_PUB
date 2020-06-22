from django.urls import path
from .views import *

urlpatterns = [
    path('ledger', index, name='ledger')
]