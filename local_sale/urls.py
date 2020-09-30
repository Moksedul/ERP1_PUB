from django.urls import path
from django.views.i18n import JavaScriptCatalog
from .views import sale_create, LocalSaleList, LocalSaleDelete, sale_update

urlpatterns = [
    path('add_local_sale', sale_create, name='add-local-sale'),
    path('local_sale_list', LocalSaleList.as_view(), name='local-sale-list'),
    path('local_sale/<int:pk>/delete', LocalSaleDelete.as_view(), name='delete-local-sale'),
    path('local_sale/<int:pk>/update', sale_update, name='update-local-sale'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
