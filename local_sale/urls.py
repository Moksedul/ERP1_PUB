from django.urls import path
from django.views.i18n import JavaScriptCatalog
from .views import sale_create, SaleCreate, LocalSaleList

urlpatterns = [
    path('add_local_sale', SaleCreate.as_view(), name='add-local-sale'),
    path('local_sale_list', LocalSaleList.as_view(), name='local-sale-list'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
