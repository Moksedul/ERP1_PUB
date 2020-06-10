from django.urls import path
from .views import PaymentCreate
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('add_payment', PaymentCreate.as_view(), name='add-payment'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
